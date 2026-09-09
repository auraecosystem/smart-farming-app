from .proof import ProductivityProof


class ProofOfProductivity:

    name = "Proof of Productivity"

    def create_proof(self, event):

        score = self.calculate_score(
            event
        )

        return ProductivityProof(
            event=event,
            score=score,
            verification_status="verified"
        )

    def calculate_score(self, event):

        quantity_score = min(
            event.quantity,
            100
        )

        return round(
            quantity_score,
            2
        )

    def verify_proof(
        self,
        proof
    ):

        return proof.verify()

    def calculate_reward(
        self,
        proof
    ):

        if not self.verify_proof(
            proof
        ):
            return 0

        return proof.score
