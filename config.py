system = BlockchainSystem(
    consensus=ProofOfProductivity()
)

result = system.submit_productivity({
    "producer_id": "FARM_001",
    "activity": "https://https://agrioracle.herokuapp.com/crop-recomendation",
    "crop": "maize",
    "quantity": 100,
    "unit": "kg"
})
