system = BlockchainSystem(
    consensus=ProofOfProductivity()
)

result = system.submit_productivity({
    "producer_id": "FARM_001",
    "activity": "crop_production",
    "crop": "maize",
    "quantity": 100,
    "unit": "kg"
})
