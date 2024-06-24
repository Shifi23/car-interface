from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.interface.database import get_db
from backend.interface.models import Controls
from sqlalchemy.orm import Session
from typing import Annotated, List
from datetime import datetime
from backend.interface.controls.controls import test, UnlockCar

class ControlStatusesBase(BaseModel):
    locked: bool = False
    lights_on: bool = False
    engine_on: bool = False

class ControlStatuses(ControlStatusesBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

db_dependany = Annotated[Session, Depends(get_db)]
router = APIRouter(tags=["Controls"])

def get_latest_iteration(db: db_dependany):
    if not db.query(Controls).order_by(Controls.id.desc()).first():
        db_record = Controls(**ControlStatusesBase().model_dump())
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        return db.query(Controls).order_by(Controls.id.desc()).first().__dict__
    else:
        return db.query(Controls).order_by(Controls.id.desc()).first().__dict__
    

@router.get("/status", response_model=ControlStatuses)
async def get_control_statuses(db: db_dependany):
    statues = get_latest_iteration(db)
    return statues

@router.post("/lock")
async def lock_car(db: db_dependany):
    db_record = ControlStatusesBase(**db.query(Controls).order_by(Controls.id.desc()).first().__dict__).model_dump()
    update_status = {"locked": True}
    db_record |= update_status
    db_record = Controls(**db_record)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return 200

@router.delete("/lock")
async def unlock_car(db: db_dependany):
    db_record = ControlStatusesBase(**db.query(Controls).order_by(Controls.id.desc()).first().__dict__).model_dump()
    UnlockCar()
    update_status = {"locked": False}
    db_record |= update_status
    db_record = Controls(**db_record)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return 200

@router.post("/lights")
async def turn_on_lights(db: db_dependany):
    db_record = ControlStatusesBase(**db.query(Controls).order_by(Controls.id.desc()).first().__dict__).model_dump()
    test()
    update_status = {"lights_on": True}
    db_record |= update_status
    db_record = Controls(**db_record)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return 200

@router.delete("/lights")
async def turn_off_lights(db: db_dependany):
    db_record = ControlStatusesBase(**db.query(Controls).order_by(Controls.id.desc()).first().__dict__).model_dump()
    update_status = {"lights_on": False}
    db_record |= update_status
    db_record = Controls(**db_record)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return 200

@router.post("/engine")
async def turn_on_engine(db: db_dependany):
    db_record = ControlStatusesBase(**db.query(Controls).order_by(Controls.id.desc()).first().__dict__).model_dump()
    update_status = {"engine_on": True}
    db_record |= update_status
    db_record = Controls(**db_record)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return 200

@router.delete("/engine")
async def turn_off_engine(db: db_dependany):
    db_record = ControlStatusesBase(**db.query(Controls).order_by(Controls.id.desc()).first().__dict__).model_dump()
    update_status = {"engine_on": False}
    db_record |= update_status
    db_record = Controls(**db_record)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return 200
