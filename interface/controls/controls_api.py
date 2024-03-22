from fastapi import APIRouter, Depends
from pydantic import BaseModel
from interface.database import get_db
from interface.models import Controls
from sqlalchemy.orm import Session
from typing import Annotated

class ControlStatusesBase(BaseModel):
    locked: bool
    lights_on: bool
    engine_on: bool

class ControlStatuses(ControlStatusesBase):
    id: int

    class Config:
        from_attributes = True

db_dependany = Annotated[Session, Depends(get_db)]
router = APIRouter(tags=["Controls"])

@router.get("/status")
async def get_control_statuses():
    return []

@router.post("/lock", response_model=ControlStatuses)
async def lock_car(status: ControlStatusesBase, db: db_dependany):
    db_lock = Controls(ControlStatusesBase(locked=False, ))
    db.add(db_lock)
    db.commit()
    db.refresh(db_lock)
    return db_lock

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
