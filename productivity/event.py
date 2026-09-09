from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Any


@dataclass
class ProductivityEvent:

    producer_id: str
    activity: str
    quantity: float
    unit: str

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    timestamp: str = field(
        default_factory=lambda:
        datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self):

        return {
            "producer_id": self.producer_id,
            "activity": self.activity,
            "quantity": self.quantity,
            "unit": self.unit,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }
