from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel
from backend.interface.database import get_db, get_latest_iteration, update_db
from backend.interface.models import Controls
from sqlalchemy.orm import Session
from typing import Annotated, List
from datetime import datetime
from backend.interface.controls.controls import RelayController

class ControlStatusesBase(BaseModel):
    enabled: bool = False
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


@router.get("/status", response_model=ControlStatuses)
async def get_control_statuses(db: db_dependany):
    statues = get_latest_iteration(db, Controls, ControlStatusesBase)
    return statues

@router.post("/enable", responses={200: {"description": "success"}, 400:{"description": "handshake with relay controller unsuccessful"}})
async def enable_controls(db: db_dependany):
    try:
        global controller
        controller = RelayController()
        update_db(db, Controls, ControlStatusesBase, newData={"enabled": True})
    except Exception as e:
        controller = None
        return Response(content="handshake with relay controller unsuccessful", status_code=400)

    return 200

@router.delete("/enable", responses={200: {"description": "success"}, 400:{"description": "controls was not enabled"}})
async def disable_controls(db: db_dependany):
    try:
        global controller
        controller.__del__()
        update_db(db, Controls, ControlStatusesBase, newData={"enabled": False})
    except Exception as e:
        controller = None
        return Response(content="controls was not disabled", status_code=400)
        
    return 200

@router.post("/lock", responses={200: {"description": "success"}, 400:{"description": "controls was not enabled"}})
async def lock_car(db: db_dependany):
    if controller:
        controller.lock_car()
        update_db(db, Controls, ControlStatusesBase, newData={"locked": True} )
        return 200
    else:
        return Response(content="controls not enabled", status_code=400)

@router.delete("/lock", responses={200: {"description": "success"}, 400:{"description": "controls was not enabled"}})
async def unlock_car(db: db_dependany):
    if controller:
        controller.unlock_car()
        update_db(db, Controls, ControlStatusesBase, newData={"locked": True})
        return 200
    else:
        return Response(content="controls not enabled", status_code=400)

@router.post("/lights", responses={200: {"description": "success"}, 400:{"description": "controls was not enabled"}})
async def turn_on_lights(db: db_dependany):
    if controller:
        controller.turn_on_parking_lights()
        update_db(db, Controls, ControlStatusesBase, newData={"lights_on": True})
        return 200
    else:
        return Response(content="controls not enabled", status_code=400)

@router.delete("/lights", responses={200: {"description": "success"}, 400:{"description": "controls was not enabled"}})
async def turn_off_lights(db: db_dependany):
    if controller:
        controller.turn_off_parking_lights()
        update_db(db, Controls, ControlStatusesBase, newData={"lights_on": False})
        return 200
    else:
        return Response(content="controls not enabled", status_code=400)

@router.post("/engine", responses={200: {"description": "success"}, 400:{"description": "controls was not enabled"}})
async def turn_on_engine(db: db_dependany):
    if controller:
        controller.start_engine()
        update_db(db, Controls, ControlStatusesBase, newData={"engine_on": True})
        return 200
    else:
        return Response(content="controls not enabled", status_code=400)

@router.delete("/engine", responses={200: {"description": "success"}, 400:{"description": "controls was not enabled"}})
async def turn_off_engine(db: db_dependany):
    if controller:
        controller.stop_engine()
        update_db(db, Controls, ControlStatusesBase, newData={"engine_on": False})
        return 200
    else:
        return Response(content="controls not enabled", status_code=400)
