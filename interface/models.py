from interface.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float

class Controls(Base):
    __tablename__ = "controls"

    id = Column(Integer, primary_key=True, index=True)
    locked = Column(Boolean)
    lights_on = Column(Boolean)
    engine_on = Column(Boolean)