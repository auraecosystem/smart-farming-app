class ProofOfStake(ConsensusEngine):

    def select_validator(self, participants):
        return max(
            participants,
            key=lambda validator: validator["stake"]
        )

    def validate_block(self, block):
        return True

    def calculate_reward(self, participant):
        return 5
