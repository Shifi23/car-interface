from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel
from backend.interface.database import get_db
from backend.interface.models import Controls
from sqlalchemy.orm import Session
from typing import Annotated, List
from datetime import datetime
from backend.interface.controls.controls import RelayController

class ControlStatusesBase(BaseModel):
    locked: bool = False
    lights_on: bool = False
    engine_on: bool = False

class ControlStatuses(ControlStatusesBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

controller = None

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

def update_db(db: db_dependany, status):
    if not db.query(Controls).order_by(Controls.id.desc()).first():
        get_latest_iteration(db)
    db_record = ControlStatusesBase(**db.query(Controls).order_by(Controls.id.desc()).first().__dict__).model_dump()
    db_record |= status
    db_record = Controls(**db_record)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)





@router.get("/status", response_model=ControlStatuses)
async def get_control_statuses(db: db_dependany):
    statues = get_latest_iteration(db)
    return statues

@router.post("/enable", responses={200: {"description": "success"}, 400:{"description": "handshake with relay controller unsuccessful"}})
async def enable_controls():
    try:
        global controller
        controller = RelayController()
    except Exception as e:
        controller = None
        return Response(content="handshake with relay controller unsuccessful", status_code=400)

    return 200

@router.delete("/enable", responses={200: {"description": "success"}, 400:{"description": "controls was not enabled"}})
async def disable_controls():
    try:
        global controller
        controller.__del__()
    except Exception as e:
        controller = None
        return Response(content="controls was not enabled", status_code=400)
        
    return 200

@router.post("/lock", responses={200: {"description": "success"}, 400:{"description": "controls was not enabled"}})
async def lock_car(db: db_dependany):
    if controller:
        controller.lock_car()
        update_db(db, status={"locked": True})
        return 200
    else:
        return Response(content="controls not enabled", status_code=400)

@router.delete("/lock", responses={200: {"description": "success"}, 400:{"description": "controls was not enabled"}})
async def unlock_car(db: db_dependany):
    if controller:
        controller.unlock_car()
        update_db(db, status={"locked": True})
        return 200
    else:
        return Response(content="controls not enabled", status_code=400)

@router.post("/lights", responses={200: {"description": "success"}, 400:{"description": "controls was not enabled"}})
async def turn_on_lights(db: db_dependany):
    if controller:
        controller.turn_on_parking_lights()
        update_db(db, status={"lights_on": True})
        return 200
    else:
        return Response(content="controls not enabled", status_code=400)

@router.delete("/lights", responses={200: {"description": "success"}, 400:{"description": "controls was not enabled"}})
async def turn_off_lights(db: db_dependany):
    if controller:
        controller.turn_on_parking_lights()
        update_db(db, status={"lights_on": False})
        return 200
    else:
        return Response(content="controls not enabled", status_code=400)

@router.post("/engine", responses={200: {"description": "success"}, 400:{"description": "controls was not enabled"}})
async def turn_on_engine(db: db_dependany):
    if controller:
        controller.start_engine()
        update_db(db, status={"engine_on": True})
        return 200
    else:
        return Response(content="controls not enabled", status_code=400)

@router.delete("/engine", responses={200: {"description": "success"}, 400:{"description": "controls was not enabled"}})
async def turn_off_engine(db: db_dependany):
    if controller:
        controller.stop_engine()
        update_db(db, status={"engine_on": False})
        return 200
    else:
        return Response(content="controls not enabled", status_code=400)
