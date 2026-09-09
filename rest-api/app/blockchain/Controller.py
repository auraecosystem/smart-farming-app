from fastapi import APIRouter, HTTPException

from app.module.schemas import (
    ProductivityEventRequest,
    FarmCreateRequest,
)

from app.module.service import SmartFarmService


router = APIRouter(
    prefix="/api/v1",
    tags=["Smart Farm"]
)


service = SmartFarmService()


# ============================================================
# HEALTH
# ============================================================

@router.get("/health")
def health_check():

    return {
        "status": "ok",
        "service": "Smart Farm REST API",
        "blockchain": "@blockchain",
        "version": "0.1.0"
    }


# ============================================================
# FARM MANAGEMENT
# ============================================================

@router.post("/farms")
def create_farm(
    request: FarmCreateRequest
):

    try:

        farm = service.create_farm(
            request
        )

        return {
            "success": True,
            "farm": farm
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.get("/farms")
def get_farms():

    farms = service.get_farms()

    return {
        "success": True,
        "count": len(farms),
        "farms": farms
    }


@router.get("/farms/{farm_id}")
def get_farm(
    farm_id: str
):

    farm = service.get_farm(
        farm_id
    )

    if farm is None:

        raise HTTPException(
            status_code=404,
            detail="Farm not found"
        )

    return {
        "success": True,
        "farm": farm
    }


# ============================================================
# PRODUCTIVITY
# ============================================================

@router.post(
    "/productivity"
)
def submit_productivity(
    request: ProductivityEventRequest
):

    try:

        result = (
            service
            .submit_productivity(
                request
            )
        )

        return {
            "success": True,
            "result": result
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


# ============================================================
# BLOCKCHAIN
# ============================================================

@router.get(
    "/blockchain"
)
def get_blockchain():

    chain = (
        service
        .get_blockchain()
    )

    return {
        "success": True,
        "length": len(chain),
        "chain": chain
    }


@router.get(
    "/blockchain/blocks/{index}"
)
def get_block(
    index: int
):

    block = (
        service
        .get_block(index)
    )

    if block is None:

        raise HTTPException(
            status_code=404,
            detail="Block not found"
        )

    return {
        "success": True,
        "block": block
    }


@router.get(
    "/blockchain/validate"
)
def validate_blockchain():

    valid = (
        service
        .validate_blockchain()
    )

    return {
        "success": True,
        "valid": valid
    }


# ============================================================
# REWARDS
# ============================================================

@router.get(
    "/rewards/{producer_id}"
)
def get_rewards(
    producer_id: str
):

    reward = (
        service
        .get_rewards(
            producer_id
        )
    )

    return {
        "success": True,
        "producer_id": producer_id,
        "reward": reward
    }
