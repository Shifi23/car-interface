from backend.interface.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, TIMESTAMP
import datetime

class Controls(Base):
    __tablename__ = "controls"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow())
    enabled = Column(Boolean)
    locked = Column(Boolean)
    lights_on = Column(Boolean)
    engine_on = Column(Boolean)

class Energy(Base):

    __tablename__ = "energy"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow())
    battery_percentage = Column(Float)
    battery_capacity = Column(Integer)
    estimated_time = Column(Float)
    dc_power_out = Column(Integer)
    usb_c_power_out = Column(Integer)
    dc_power_in = Column(Integer)
    solar_power_in = Column(Integer)



