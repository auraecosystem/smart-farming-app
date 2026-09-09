from abc import ABC, abstractmethod


class ConsensusEngine(ABC):

    @abstractmethod
    def select_validator(self, participants):
        pass

    @abstractmethod
    def validate_block(self, block):
        pass

    @abstractmethod
    def calculate_reward(self, participant):
        pass
class ProofOfWork(ConsensusEngine):

    def select_validator(self, participants):
        return max(
            participants,
            key=lambda miner: miner["hash_power"]
        )

    def validate_block(self, block):
        return block.hash.startswith(
            "0" * block.difficulty
        )

    def calculate_reward(self, participant):
        return 10
