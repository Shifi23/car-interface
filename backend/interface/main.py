from fastapi import FastAPI
from backend.interface.controls import controls_api
from backend.interface.obd import obd_api
from backend.interface.ecoflow import ecoflow_api
from backend.interface.keyless import keyless_api
from fastapi.middleware.cors import CORSMiddleware
from backend.interface.database import engine
import backend.interface.models
from backend.interface.tasks import test
from backend.interface.celery_utils import make_celery


backend.interface.models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Car Interface APIs", version="0.2.0", docs_url="/")

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins
)


make_celery()




@app.get("/version", tags=["Car-Interface"])
async def get_car_interface_version():
    task = test.delay(1,2)
    return {"version": "0.2.0", "result": task.id()}
        
## add routes here
app.include_router(
    controls_api.router,
    prefix="/controls"
)

app.include_router(
    obd_api.router,
    prefix="/obd"
)

app.include_router(
    ecoflow_api.router,
    prefix="/ecoflow"
)

app.include_router(
    keyless_api.router,
    prefix="/keyless"
)

