import hashlib
import json


class ProductivityProof:

    def __init__(
        self,
        event,
        score,
        verification_status="pending"
    ):

        self.event = event
        self.score = score
        self.verification_status = (
            verification_status
        )

        self.event_hash = self.generate_hash()

    def generate_hash(self):

        payload = json.dumps(
            self.event.to_dict(),
            sort_keys=True
        )

        return hashlib.sha256(
            payload.encode()
        ).hexdigest()

    def verify(self):

        return (
            self.verification_status
            == "verified"
        )

    def to_dict(self):

        return {
            "event_hash": self.event_hash,
            "score": self.score,
            "verification_status":
                self.verification_status
        }
