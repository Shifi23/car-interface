from fastapi import APIRouter, Depends, Response, BackgroundTasks
from pydantic import BaseModel
from backend.interface.database import get_db, get_latest_iteration, update_db
from backend.interface.keyless.scan import start_scan, stop_scan
from backend.interface.models import Keyless
from sqlalchemy.orm import Session
from typing import Annotated, List
from datetime import datetime

class KeylessStatusesBase(BaseModel):
    enabled: bool = False
    phone_nearby: bool = False

class KeylessStatus(KeylessStatusesBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

db_dependany = Annotated[Session, Depends(get_db)]
router = APIRouter(tags=["Keyless"])

@router.get("/status", response_model=KeylessStatus)
async def get_keyless_service_status(db: db_dependany):
    statues = get_latest_iteration(db, Keyless, KeylessStatusesBase)
    return statues

@router.post("/start")
async def start_keyless_service(db: db_dependany, background_tasks: BackgroundTasks):
    background_tasks.add_task(start_scan)
    update_db(db, Keyless, KeylessStatusesBase, newData={"enabled": True})
    return 200

@router.delete("/stop")
async def stop_keyless_service(db: db_dependany, background_tasks: BackgroundTasks):
    # background_tasks.add_task(stop_scan)
    await stop_scan()
    update_db(db, Keyless, KeylessStatusesBase, newData={"enabled": False})
    return 200
