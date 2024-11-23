from sqlalchemy import Integer, String, DateTime
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()

class TaxiPool(Base):
    __tablename__ = "TaxiPool"
    id = Column(Integer, primary_key=True)
    start_position = Column(String)
    end_position = Column(String)
    total_people = Column(Integer)
    start_time = Column(DateTime)
    creator_id = Column(String)
    creator_nickname = Column(String)
    created_at = Column(DateTime, server_default=current_timestamp())

class PoolMember(Base):
    __tablename__ = "PoolMember"
    id = Column(Integer, primary_key=True)
    taxi_id = Column(String)
    user_id = Column(String)
    created_at = Column(DateTime, server_default=current_timestamp())