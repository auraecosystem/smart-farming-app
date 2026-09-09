class DelegatedProofOfStake(ConsensusEngine):

    def select_validator(self, participants):
        return max(
            participants,
            key=lambda delegate: delegate["votes"]
        )

    def validate_block(self, block):
        return True

    def calculate_reward(self, participant):
        return 3
