from blockchain.chain import Blockchain
from consensus.pow import ProofOfWork
from consensus.pos import ProofOfStake
from consensus.dpos import DelegatedProofOfStake
from consensus.pop import ProofOfProductivity


def main():

    print("=" * 60)
    print("        @BLOCKCHAIN PRODUCTIVITY CHAIN")
    print("=" * 60)

    # Select consensus mechanism
    consensus = ProofOfProductivity()

    # Initialize blockchain
    blockchain = Blockchain(
        consensus=consensus
    )

    # Example productivity event
    productivity_event = {
        "producer_id": "FARMER_001",
        "activity": "crop_production",
        "crop": "maize",
        "quantity": 100,
        "unit": "kg",
        "timestamp": "2026-07-25T00:00:00Z"
    }

    # Create productivity proof
    proof = consensus.create_proof(
        productivity_event
    )

    # Create and validate block
    block = blockchain.create_block(
        data=productivity_event,
        proof=proof
    )

    # Add block
    blockchain.add_block(block)

    # Calculate reward
    reward = consensus.calculate_reward(
        productivity_event
    )

    print("\nProductivity Event:")
    print(productivity_event)

    print("\nProductivity Proof:")
    print(proof)

    print("\nBlock:")
    print(block)

    print("\nReward:")
    print(reward)

    print("\nBlockchain Valid:")
    print(blockchain.is_valid())


if __name__ == "__main__":
    main()
