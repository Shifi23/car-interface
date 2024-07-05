from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = "sqlite:///./car.db"

engine = create_engine(URL_DATABASE, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# helper functions:

def get_latest_iteration(db, model, baseModel):
    if not db.query(model).order_by(model.id.desc()).first():
        db_record = model(**baseModel().model_dump())
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        return db.query(model).order_by(model.id.desc()).first().__dict__
    else:
        return db.query(model).order_by(model.id.desc()).first().__dict__
    

def update_db(db, model, baseModel, newData):
    if not db.query(model).order_by(model.id.desc()).first():
        get_latest_iteration(db)
    db_record = baseModel(**db.query(model).order_by(model.id.desc()).first().__dict__).model_dump()
    db_record |= newData
    db_record = model(**db_record)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    