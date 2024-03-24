from interface.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, TIMESTAMP
import datetime

class Controls(Base):
    __tablename__ = "controls"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow())
    locked = Column(Boolean)
    lights_on = Column(Boolean)
    engine_on = Column(Boolean)