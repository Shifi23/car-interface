from fastapi import FastAPI
from backend.interface.controls import controls_api
from backend.interface.obd import obd_api
from fastapi.middleware.cors import CORSMiddleware
from backend.interface.database import engine
import backend.interface.models

backend.interface.models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Car Interface APIs", version="0.0.1", docs_url="/")

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins
)




@app.get("/version", tags=["Car-Interface"])
async def get_car_interface_version():
    return {"version": "0.0.1"}

## add routes here
app.include_router(
    controls_api.router,
    prefix="/controls"
)

app.include_router(
    obd_api.router,
    prefix="/obd"
)
