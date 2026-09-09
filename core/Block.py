class BlockchainSystem:

    def __init__(self, consensus):
        self.consensus = consensus
        self.blockchain = Blockchain()
        self.reward_engine = RewardEngine()

    def submit_productivity(self, event):

        # 1. Generate proof
        proof = self.consensus.create_proof(event)

        # 2. Verify proof
        if not self.consensus.verify_proof(
            event,
            proof
        ):
            raise ValueError(
                "Productivity proof rejected"
            )

        # 3. Create block
        block = self.blockchain.create_block(
            data=event,
            proof=proof
        )

        # 4. Validate block
        if not self.consensus.validate_block(
            block
        ):
            raise ValueError(
                "Block rejected"
            )

        # 5. Add block
        self.blockchain.add_block(block)

        # 6. Calculate reward
        reward = self.reward_engine.calculate(
            event
        )

        return {
            "block": block,
            "proof": proof,
            "reward": reward
        }
