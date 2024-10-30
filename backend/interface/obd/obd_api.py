from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel
from backend.interface.database import get_db, get_latest_iteration, update_db
from backend.interface.models import OBD
from sqlalchemy.orm import Session
from typing import Annotated, List
from datetime import datetime
from backend.interface.obd.obd_manager import ObdManager

class ObdDataBase(BaseModel):
    engine_running: bool = False
    voltage: float = 0
    rpm: float = 0
    speed: float = 0
    coolant_temp: float = 0
    intake_temp: float = 0
    mass_airflow_rate: float = 0
    throttle_position: float = 0
    engine_load: float = 0
    dtc: str = ""

class ObdData(ObdDataBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

db_dependany = Annotated[Session, Depends(get_db)]
router = APIRouter(tags=["OBD-II data"])

@router.get("/data", response_model=ObdData)
async def get_odb_data(db: db_dependany):
    data = get_latest_iteration(db, OBD, ObdDataBase)
    return data