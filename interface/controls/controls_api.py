from fastapi import APIRouter

router = APIRouter(tags=["Controls"])

@router.get("/status")
async def get_control_statuses():
    return []

@router.post("/lock")
async def lock_car():
    return 200

@router.delete("/lock")
async def unlock_car():
    return 200

@router.post("/lights")
async def turn_on_lights():
    return 200

@router.delete("/lights")
async def turn_off_lights():
    return 200

@router.post("/engine")
async def turn_on_engine():
    return 200

@router.delete("/engine")
async def turn_off_engine():
    return 200
