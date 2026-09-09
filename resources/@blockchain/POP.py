class ProofOfProductivity(ConsensusEngine):

    def select_validator(self, participants):
        return max(
            participants,
            key=lambda producer: producer["productivity_score"]
        )

    def validate_block(self, block):
        return (
            block.productivity_proof is not None
        )

    def calculate_reward(self, participant):
        productivity = participant[
            "productivity_score"
        ]

        return productivity
