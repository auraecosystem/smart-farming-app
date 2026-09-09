from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from uuid import uuid4
from datetime import datetime, timezone


class VerificationStatus(str, Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"


@dataclass
class Crop:
    crop_id: str
    name: str
    category: str
    season: str


@dataclass
class Farm:
    farm_id: str
    owner_id: str
    name: str
    location: str
    area_hectares: Decimal


@dataclass
class Production:
    production_id: str
    farm_id: str
    crop_id: str
    predicted_yield_kg: Decimal
    actual_yield_kg: Decimal | None = None
    quality_grade: str | None = None
    status: VerificationStatus = VerificationStatus.PENDING
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass
class AgriculturalReceipt:
    receipt_id: str
    production_id: str
    farm_id: str
    crop_id: str
    quantity_kg: Decimal
    market_value: Decimal
    status: str = "active"


class KAVP:

    def __init__(self):
        self.crops = {}
        self.farms = {}
        self.productions = {}
        self.receipts = {}

    def register_crop(self, crop: Crop):
        self.crops[crop.crop_id] = crop

    def register_farm(self, farm: Farm):
        self.farms[farm.farm_id] = farm

    def create_production(
        self,
        farm_id: str,
        crop_id: str,
        predicted_yield_kg: Decimal
    ):
        if farm_id not in self.farms:
            raise ValueError("Farm does not exist")

        if crop_id not in self.crops:
            raise ValueError("Crop does not exist")

        production = Production(
            production_id=f"PROD-{uuid4().hex[:12].upper()}",
            farm_id=farm_id,
            crop_id=crop_id,
            predicted_yield_kg=predicted_yield_kg
        )

        self.productions[
            production.production_id
        ] = production

        return production

    def verify_production(
        self,
        production_id: str,
        actual_yield_kg: Decimal,
        quality_grade: str
    ):
        production = self.productions.get(production_id)

        if not production:
            raise ValueError("Production record not found")

        if actual_yield_kg <= 0:
            raise ValueError("Yield must be positive")

        if actual_yield_kg > production.predicted_yield_kg * Decimal("1.5"):
            raise ValueError(
                "Yield exceeds plausible verification threshold"
            )

        production.actual_yield_kg = actual_yield_kg
        production.quality_grade = quality_grade
        production.status = VerificationStatus.VERIFIED

        return production

    def issue_arc(
        self,
        production_id: str,
        market_price_per_kg: Decimal
    ):
        production = self.productions.get(production_id)

        if not production:
            raise ValueError("Production not found")

        if production.status != VerificationStatus.VERIFIED:
            raise ValueError(
                "Production must be verified before ARC issuance"
            )

        value = (
            production.actual_yield_kg
            * market_price_per_kg
        )

        receipt = AgriculturalReceipt(
            receipt_id=f"ARC-{uuid4().hex[:12].upper()}",
            production_id=production.production_id,
            farm_id=production.farm_id,
            crop_id=production.crop_id,
            quantity_kg=production.actual_yield_kg,
            market_value=value
        )

        self.receipts[
            receipt.receipt_id
        ] = receipt

        return receipt
