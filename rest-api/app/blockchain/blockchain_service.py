from datetime import datetime, timezone

from .block import Block
from .chain import Blockchain
from .productivity import ProductivityProof
from .consensus import ProofOfProductivity
from .rewards import RewardEngine


class BlockchainService:

    def __init__(self):

        self.blockchain = Blockchain()

        self.consensus = (
            ProofOfProductivity()
        )

        self.reward_engine = (
            RewardEngine()
        )

    # =========================================================
    # PRODUCTIVITY
    # =========================================================

    def submit_productivity_event(
        self,
        event
    ):

        self._validate_event(
            event
        )

        proof = (
            self.consensus
            .create_proof(
                event
            )
        )

        if not self.consensus.verify_proof(
            proof
        ):

            raise ValueError(
                "Productivity proof "
                "verification failed"
            )

        block = self._create_block(
            event,
            proof
        )

        self.blockchain.add_block(
            block
        )

        reward = (
            self.reward_engine
            .calculate_reward(
                proof
            )
        )

        return {
            "event": event,
            "proof": proof.to_dict(),
            "block": block.to_dict(),
            "reward": reward,
            "timestamp":
                datetime.now(
                    timezone.utc
                ).isoformat()
        }

    # =========================================================
    # BLOCK CREATION
    # =========================================================

    def _create_block(
        self,
        event,
        proof
    ):

        previous_block = (
            self.blockchain
            .get_latest_block()
        )

        block = Block(
            index=(
                previous_block.index
                + 1
            ),
            timestamp=(
                datetime.now(
                    timezone.utc
                ).isoformat()
            ),
            data={
                "type":
                    "productivity",
                "event":
                    event,
                "proof":
                    proof.to_dict()
            },
            previous_hash=(
                previous_block.hash
            )
        )

        return block

    # =========================================================
    # VALIDATION
    # =========================================================

    def _validate_event(
        self,
        event
    ):

        required = [
            "producer_id",
            "activity",
            "crop",
            "quantity",
            "unit"
        ]

        for field in required:

            if field not in event:

                raise ValueError(
                    f"Missing required "
                    f"field: {field}"
                )

        if event["quantity"] <= 0:

            raise ValueError(
                "Quantity must be "
                "greater than zero"
            )

    # =========================================================
    # BLOCKCHAIN API
    # =========================================================

    def get_chain(self):

        return [
            block.to_dict()
            for block in
            self.blockchain.chain
        ]

    def get_block(
        self,
        index
    ):

        for block in (
            self.blockchain.chain
        ):

            if block.index == index:

                return block.to_dict()

        return None

    def validate_chain(self):

        return (
            self.blockchain
            .is_valid()
        )

    # =========================================================
    # REWARDS
    # =========================================================

    def get_rewards(
        self,
        producer_id
    ):

        return (
            self.reward_engine
            .get_rewards(
                producer_id
            )
        )
