from flask import g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.models import Base

def init_db(database_uri :str):
    engine = create_engine(database_uri)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    def get_db():
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = SessionLocal()
        return db
    
    return engine, get_db