from productivity.event import (
    ProductivityEvent
)

from consensus.pop import (
    ProofOfProductivity
)


def main():

    event = ProductivityEvent(
        producer_id="FARM_001",
        activity="crop_production",
        quantity=100,
        unit="kg",
        metadata={
            "crop": "maize"
        }
    )

    consensus = ProofOfProductivity()

    proof = consensus.create_proof(
        event
    )

    reward = consensus.calculate_reward(
        proof
    )

    print(
        "Producer:",
        event.producer_id
    )

    print(
        "Activity:",
        event.activity
    )

    print(
        "Productivity Proof:",
        proof.to_dict()
    )

    print(
        "Reward:",
        reward
    )


if __name__ == "__main__":
    main()
