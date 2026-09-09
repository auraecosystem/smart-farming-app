import hashlib
import random
import time


# ============================================================
# 1. CONSENSUS MECHANISM SIMULATION
# ============================================================

def simulate_consensus():
    print("=" * 60)
    print("CONSENSUS MECHANISM SIMULATION")
    print("=" * 60)

    # --------------------------------------------------------
    # Proof of Work
    # --------------------------------------------------------
    print("\n>>> 1. Proof of Work (PoW) Simulation")

    miners = {
        "MinerA": {"power": random.randint(1, 100)},
        "MinerB": {"power": random.randint(1, 100)},
        "MinerC": {"power": random.randint(1, 100)},
    }

    pow_winner = max(
        miners.items(),
        key=lambda x: x[1]["power"]
    )

    print("\nMiners and their computational power:")

    for name, stats in miners.items():
        print(f"  {name}: Power = {stats['power']}")

    print(
        f"\nSelected Miner: {pow_winner[0]} "
        f"(Highest simulated computational power)"
    )

    print(
        "Explanation: In a real PoW blockchain, miners compete by "
        "performing computational work to find a valid hash."
    )

    # --------------------------------------------------------
    # Proof of Stake
    # --------------------------------------------------------
    print("\n>>> 2. Proof of Stake (PoS) Simulation")

    stakers = {
        "StakerA": {"stake": random.randint(1, 100)},
        "StakerB": {"stake": random.randint(1, 100)},
        "StakerC": {"stake": random.randint(1, 100)},
    }

    pos_winner = max(
        stakers.items(),
        key=lambda x: x[1]["stake"]
    )

    print("\nStakers and their stake:")

    for name, stats in stakers.items():
        print(f"  {name}: Stake = {stats['stake']}")

    print(
        f"\nSelected Validator: {pos_winner[0]} "
        f"(Highest simulated stake)"
    )

    print(
        "Explanation: In PoS, validators are selected according to "
        "stake and protocol-specific validator-selection rules."
    )

    # --------------------------------------------------------
    # Delegated Proof of Stake
    # --------------------------------------------------------
    print("\n>>> 3. Delegated Proof of Stake (DPoS) Simulation")

    delegates = {
        "Delegate1": {"votes": 0},
        "Delegate2": {"votes": 0},
        "Delegate3": {"votes": 0},
    }

    voters = [
        "Voter1",
        "Voter2",
        "Voter3",
        "Voter4",
        "Voter5",
    ]

    print("\nVoting process:")

    for voter in voters:
        selected_delegate = random.choice(
            list(delegates.keys())
        )

        delegates[selected_delegate]["votes"] += 1

        print(
            f"  {voter} voted for {selected_delegate}"
        )

    dpos_winner = max(
        delegates.items(),
        key=lambda x: x[1]["votes"]
    )

    print("\nDelegates and their votes:")

    for name, stats in delegates.items():
        print(
            f"  {name}: Votes = {stats['votes']}"
        )

    print(
        f"\nSelected Delegate: {dpos_winner[0]} "
        f"(Most votes)"
    )

    print(
        "Explanation: In DPoS, token holders vote for delegates "
        "who participate in block production and validation."
    )


# ============================================================
# 2. BLOCK CLASS
# ============================================================

class Block:

    def __init__(
        self,
        index,
        timestamp,
        data,
        previous_hash
    ):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0

        self.hash = self.compute_hash()

    def compute_hash(self):

        block_string = (
            f"{self.index}"
            f"{self.timestamp}"
            f"{self.data}"
            f"{self.previous_hash}"
            f"{self.nonce}"
        )

        return hashlib.sha256(
            block_string.encode()
        ).hexdigest()

    def mine_block(self, difficulty):

        print(
            f"\nMining Block {self.index} "
            f"with difficulty = {difficulty}"
        )

        start_time = time.time()

        target = "0" * difficulty

        while not self.hash.startswith(target):

            self.nonce += 1

            self.hash = self.compute_hash()

        end_time = time.time()

        print("\nBlock mined successfully!")

        print("Index:", self.index)
        print("Nonce:", self.nonce)
        print("Hash:", self.hash)

        print(
            "Time taken:",
            round(end_time - start_time, 4),
            "seconds"
        )


# ============================================================
# 3. BLOCKCHAIN
# ============================================================

class Blockchain:

    def __init__(self, difficulty=4):

        self.difficulty = difficulty

        self.chain = [
            self.create_genesis_block()
        ]

    def create_genesis_block(self):

        return Block(
            0,
            time.time(),
            "Genesis Block",
            "0"
        )

    def add_block(self, data):

        previous_block = self.chain[-1]

        new_block = Block(
            len(self.chain),
            time.time(),
            data,
            previous_block.hash
        )

        new_block.mine_block(
            self.difficulty
        )

        self.chain.append(new_block)

    def is_valid(self):

        for i in range(1, len(self.chain)):

            current_block = self.chain[i]

            previous_block = self.chain[i - 1]

            # Check whether the current hash is correct
            if current_block.hash != current_block.compute_hash():

                print(
                    f"Invalid hash detected "
                    f"at Block {current_block.index}"
                )

                return False

            # Check whether the link to the previous block is valid
            if (
                current_block.previous_hash
                != previous_block.hash
            ):

                print(
                    f"Broken chain link detected "
                    f"at Block {current_block.index}"
                )

                return False

        return True

    def display(self):

        print("\n" + "=" * 60)
        print("BLOCKCHAIN")
        print("=" * 60)

        for block in self.chain:

            print(
                f"\nBlock {block.index}"
            )

            print(
                f"Data: {block.data}"
            )

            print(
                f"Hash: {block.hash}"
            )

            print(
                f"Previous Hash: "
                f"{block.previous_hash}"
            )

            print(
                f"Nonce: {block.nonce}"
            )


# ============================================================
# 4. MAIN PROGRAM
# ============================================================

def main():

    # --------------------------------------------------------
    # Run consensus simulations
    # --------------------------------------------------------

    simulate_consensus()

    # --------------------------------------------------------
    # Demonstrate individual Proof of Work mining
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("INDIVIDUAL PROOF OF WORK MINING")
    print("=" * 60)

    block = Block(
        1,
        time.time(),
        "Transaction A -> B",
        "0"
    )

    block.mine_block(
        difficulty=4
    )

    # --------------------------------------------------------
    # Create blockchain
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("CREATING BLOCKCHAIN")
    print("=" * 60)

    blockchain = Blockchain(
        difficulty=4
    )

    # Add blocks
    blockchain.add_block(
        "Transaction A -> B"
    )

    blockchain.add_block(
        "Transaction B -> C"
    )

    blockchain.add_block(
        "Transaction C -> D"
    )

    blockchain.display()

    # --------------------------------------------------------
    # Check blockchain integrity
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("INITIAL INTEGRITY CHECK")
    print("=" * 60)

    if blockchain.is_valid():

        print(
            "Blockchain is VALID."
        )

    else:

        print(
            "Blockchain is INVALID."
        )

    # --------------------------------------------------------
    # Tamper with Block 1
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("TAMPERING WITH BLOCK 1")
    print("=" * 60)

    blockchain.chain[1].data = (
        "Transaction A -> HACKED"
    )

    # Recalculate the tampered block's hash
    blockchain.chain[1].hash = (
        blockchain.chain[1].compute_hash()
    )

    print(
        "Block 1 data has been modified."
    )

    print(
        "New Block 1 Hash:",
        blockchain.chain[1].hash
    )

    print(
        "Block 2 Previous Hash:",
        blockchain.chain[2].previous_hash
    )

    # --------------------------------------------------------
    # Check integrity again
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("FINAL INTEGRITY CHECK")
    print("=" * 60)

    if blockchain.is_valid():

        print(
            "Blockchain is VALID."
        )

    else:

        print(
            "Blockchain is INVALID due to tampering."
        )


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
