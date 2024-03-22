from fastapi import FastAPI
from interface.controls import controls_api
from interface.obd import obd_api
from fastapi.middleware.cors import CORSMiddleware
from interface.database import engine
import interface.models

interface.models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Car Interface APIs", version="0.0.1")

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins
)




# @app.get("/")
# async def car_interface():
#     return {"This is Shuhrat's Car"}

## add routes here
app.include_router(
    controls_api.router,
    prefix="/controls"
)

app.include_router(
    obd_api.router,
    prefix="/obd"
)
