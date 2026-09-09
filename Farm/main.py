import base64
import json
import zlib

TURNS = 720
BOARD = 10
MAX_ORDERS = 10
SHED_CAP = 100
PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL",
            "FERTILIZER")
ANIMALS = {"GOOSE": "COOP", "COW": "PASTURE", "SHEEP": "PASTURE"}
MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
PASS = {"farmer": ["PASS"], "hands": [], "market": []}

MAIN = "7015cc00acfa4922"
YARN = "dc76e4003029ac51"
YARN_CARROT = "ab9669b9abfbea4e"
MILK_GLUT = "a84d06f1d12add7c"

# (turn, feature, threshold, target tail)
DECISIONS = (
    (226, "shop_YARN_STORE", 1, YARN),
    (360, "px_CARROT", 42, YARN_CARROT),
    (433, "inv_MILK", 10067, MILK_GLUT),
)
# <!-- blob --!>
)


_ROUTES = None

# routes — лениво распаковывает 4 маршрута: MAIN целиком, остальные как (родитель, ход, суффикс)
# _shed_adjacent — проверяет, стоит ли юнит на одной из 4 клеток у сарая
# _feature — читает публичный признак для решения о переключении (YARN_STORE / цена моркови / запас молока)
# _noop — определяет, проигнорирует ли движок это действие (для поиска свободного хода под DIG)
def routes():
    """Decode lazily: only MAIN is stored whole, the rest as (parent, turn, suffix)."""
    global _ROUTES
    if _ROUTES is None:
        p = json.loads(zlib.decompress(base64.b64decode(_BLOB)).decode())
        out = {p["main"]: p["full"]}
        for t in p["tails"]:
            out[t["h"]] = out[t["parent"]][:t["at"]] + t["suffix"]
        _ROUTES = out
    return _ROUTES


def _shed_adjacent(x, y, board=BOARD):
    h = board // 2
    return (x, y) in ((h - 1, h - 1), (h, h - 1), (h - 1, h), (h, h))


def _feature(obs, name):
    if name == "shop_YARN_STORE":
        return (obs.get("town", {}).get("unlocked_shops") or []).count("YARN_STORE")
    if name == "px_CARROT":
        return obs["market"]["prices"].get("CARROT", 0)
    if name == "inv_MILK":
        return obs["market"]["inventory"].get("MILK", 0)
    return 0


def _noop(act, tile, inv, seeds, x, y, board=BOARD):
    """True when the engine will certainly ignore this action (kaggriculture.py::
    _apply_unit_action). Only used to decide whether a turn is free to reuse."""
    if not act:
        return True
    op = act[0]
    if op in MOVES:
        dx, dy = MOVES[op]
        return not (0 <= x + dx < board and 0 <= y + dy < board)
    if op == "PASS":
        return True
    if op == "DROP":
        return (not _shed_adjacent(x, y, board)) or (not inv)
    if op == "PICKUP":
        return not _shed_adjacent(x, y, board)
    if op == "PLACE":
        item = act[1] if len(act) > 1 else None
        if (item in ANIMALS and isinstance(tile, dict)
                and tile.get("kind") == ANIMALS[item] and tile.get("animal") is None):
            return inv.get(item, 0) <= 0
        if _shed_adjacent(x, y, board):
            return inv.get(item, 0) <= 0
        return True
    if tile == "LOCKED":
        return True
    isd = isinstance(tile, dict)
    kind = tile.get("kind") if isd else None
    animal = isd and tile.get("animal") is not None
    if op == "PLANT":
        return tile is not None or seeds.get(act[1] if len(act) > 1 else None, 0) <= 0
    if op == "WATER":
        return kind != "PLANT" or bool(tile.get("watered_today"))
    if op == "HARVEST":
        return (not isd) or tile.get("yield_units", 0) <= 0
    if op == "FERTILIZE":
        return kind != "PLANT" or inv.get("FERTILIZER", 0) <= 0
    if op == "DIG":
        return tile is None or animal
    if op in ("BUILD_COOP", "BUILD_PASTURE"):
        return tile is not None
    if op == "FEED":
        return (not animal) or bool(tile.get("fed_today")) or inv.get("WHEAT", 0) <= 0
    if op == "COLLECT_FERTILIZER":
        return (not animal) or (not tile.get("fertilizer_available"))
    if op == "CARE":
        return (not animal) or bool(tile.get("cared_today"))
    return True

# class Agent:
#   будущие продажи (future_sells) — сколько товара маршрут ещё продаст после этого хода
#   _switch_ok — переключение разрешено только на хвост, идентичный текущему до этого хода
#   act — главный метод: выбор хвоста, weed_dig, clamp_sells, dead_stock
# act:
#   — применяет 3 решения (YARN → CARROT → MILK) при совпадении порогов
#   — weed_dig: если юнит на сорняке и действие бесполезно — копает
#   — проекция сарая: учитывает DROP/PLACE до обработки рынка
#   — clamp_sells: отбрасывает SELL, который сарай не может выполнить
#   — dead_stock: продаёт то, что маршрут больше никогда не продаст
class Agent:
    def __init__(self):
        self.R = routes()
        self.cur = MAIN
        self._fs = None
        self._fs_for = None

    # ---- how much of each product does the rest of the route still intend to sell? ----
    def future_sells(self, item, step):
        if self._fs_for != self.cur:
            r = self.R[self.cur]
            fs = dict((p, [0] * (len(r) + 1)) for p in PRODUCTS)
            for t in range(len(r) - 1, -1, -1):
                add = {}
                for o in (r[t].get("market") or []):
                    if o and o[0] == "SELL" and o[1] in fs:
                        add[o[1]] = add.get(o[1], 0) + int(o[2])
                for p in fs:
                    fs[p][t] = fs[p][t + 1] + add.get(p, 0)
            self._fs = fs
            self._fs_for = self.cur
        a = self._fs.get(item)
        return a[step] if a and step < len(a) else 0

    def _switch_ok(self, target, turn):
        """A switch is legal only onto a tail identical to the current one so far."""
        a, b = self.R[self.cur], self.R[target]
        if a is b:
            return False
        for t in range(turn):
            if a[t] != b[t]:
                return False
        return True

    def act(self, obs):
        s = obs.get("step")
        step = int(s) if s is not None else int(obs.get("day", 0)) * 24 + int(obs.get("hour", 0))
        me = int(obs.get("player", 0))
        farm = obs["farms"][me]
        priv = obs["private"]
        tiles = farm["tiles"]
        seeds = priv.get("seeds") or {}
        invs = priv.get("inventories") or []
        shed = dict(priv.get("shed") or {})
        prices = obs["market"]["prices"]
        day = int(obs.get("day", step // 24))
        board = len(tiles) or BOARD

        for (turn, feat, thr, target) in DECISIONS:
            if turn == step and target != self.cur and self._switch_ok(target, turn):
                if _feature(obs, feat) >= thr:
                    self.cur = target

        route = self.R[self.cur]
        base = route[step] if step < len(route) else PASS
        acts = [list(base.get("farmer") or ["PASS"])] + [list(h) for h in (base.get("hands") or [])]
        market = [list(o) for o in (base.get("market") or [])]
        positions = [tuple(farm["farmer"])] + [tuple(p) for p in farm["hands"]]

        # ---- weed_dig: a wasted turn spent standing on a weed becomes a DIG ----
        for i in range(min(len(acts), len(positions))):
            x, y = positions[i]
            if not (0 <= x < board and 0 <= y < board):
                continue
            tile = tiles[y][x]
            inv = invs[i] if i < len(invs) else {}
            if (isinstance(tile, dict) and tile.get("kind") == "WEED"
                    and _noop(acts[i], tile, inv, seeds, x, y, board)):
                acts[i] = ["DIG"]

        # ---- projected shed: a same-turn DROP/PLACE lands before market processing ----
        proj = dict(shed)
        room = SHED_CAP - sum(proj.values())
        for i in range(min(len(acts), len(positions))):
            if room <= 0:
                break
            x, y = positions[i]
            inv = invs[i] if i < len(invs) else {}
            if not inv or not _shed_adjacent(x, y, board):
                continue
            a = acts[i]
            if a and a[0] == "DROP":
                for it, n in inv.items():
                    take = min(n, room)
                    if take > 0:
                        proj[it] = proj.get(it, 0) + take
                        room -= take
            elif a and a[0] == "PLACE" and len(a) > 1 and a[1] not in ANIMALS:
                it = a[1]
                take = min(int(a[2]) if len(a) > 2 else 1, inv.get(it, 0), room)
                if take > 0:
                    proj[it] = proj.get(it, 0) + take
                    room -= take

    
        avail = dict(proj)
        kept = []
        for o in market:
            if o and o[0] == "SELL":
                have = avail.get(o[1], 0)
                if have <= 0:
                    continue
                n = min(int(o[2]), have)
                if n <= 0:
                    continue
                avail[o[1]] = have - n
                kept.append(["SELL", o[1], n])
            else:
                kept.append(o)
        market = kept

        # ---- dead_stock: sell what the rest of the route will never get to ----
        planned = {}
        for o in market:
            if o and o[0] == "SELL":
                planned[o[1]] = planned.get(o[1], 0) + int(o[2])
        extra = []
        for it in PRODUCTS:
            have = proj.get(it, 0) - planned.get(it, 0)
            if have <= 0:
                continue
            surplus = have if day >= 29 else have - self.future_sells(it, step + 1)
            if surplus > 0 and prices.get(it, 0) > 1:
                extra.append(["SELL", it, surplus])
        extra.sort(key=lambda o: -prices.get(o[1], 0) * int(o[2]))

        return {"farmer": acts[0], "hands": acts[1:],
                "market": (market + extra)[:MAX_ORDERS]}


_A = None


def agent(obs):
    """A crash here forfeits the game, so any failure degrades to a legal PASS."""
    global _A
    try:
        s = obs.get("step")
        step = int(s) if s is not None else int(obs.get("day", 0)) * 24 + int(obs.get("hour", 0))
        if _A is None or step == 0:
            _A = Agent()
        return _A.act(obs)
    except Exception:
        try:
            hands = obs["farms"][int(obs.get("player", 0))].get("hands") or []
        except Exception:
            hands = []
        return {"farmer": ["PASS"], "hands": [["PASS"] for _ in hands], "market": []}
