system = BlockchainSystem(
    consensus=ProofOfProductivity()
)

result = system.submit_productivity({
    "producer_id": "FARM_001",
    "activity": "https://auraecosystem.github.io/smart-farming-app/",
    "crop": "maize",
    "quantity": 100,
    "unit": "kg"
})
