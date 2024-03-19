from fastapi import APIRouter

router = APIRouter(tags=["OBD-II data"])

@router.get("/data")
async def get_odb_data():
    return []

