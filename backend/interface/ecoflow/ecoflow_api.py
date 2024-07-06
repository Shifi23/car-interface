from fastapi import APIRouter, Depends, Response, BackgroundTasks
from pydantic import BaseModel
from backend.interface.database import get_db, get_latest_iteration, update_db
from backend.interface.ecoflow.ecoflow import start
from backend.interface.models import Energy
from sqlalchemy.orm import Session
from typing import Annotated, List
from datetime import datetime

class EnergyStatusesBase(BaseModel):
    battery_percentage: float = 0
    battery_capacity: int = 0
    estimated_time: float = 0
    dc_power_out: int = 0
    usb_c_power_out: int = 0
    dc_power_in: int = 0
    solar_power_in: int = 0

class EnergyStatus(EnergyStatusesBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

db_dependany = Annotated[Session, Depends(get_db)]
router = APIRouter(tags=["Ecoflow"])

@router.get("/status", response_model=EnergyStatus)
async def get_ecoflow_statuses(db: db_dependany):
    statues = get_latest_iteration(db, Energy, EnergyStatusesBase)
    return statues

@router.post("/start")
async def update_status_in_background(db: db_dependany, background_tasks: BackgroundTasks):
    background_tasks.add_task(start, db, Energy, EnergyStatusesBase)
    return {"message": "collecting ecoflow data in background"}
