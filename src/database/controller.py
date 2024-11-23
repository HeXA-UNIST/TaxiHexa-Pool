from sqlalchemy.orm import Session
from src.database.models import TaxiPool, PoolMember
from datetime import datetime


def create_taxi_pool(db: Session, start_position: str, end_position: str, total_people: int, start_time: datetime, creator_nickname: str, creator_id: str):
    taxi_pool = TaxiPool(
        start_position=start_position,
        end_position=end_position,
        total_people=total_people,
        start_time=start_time,
        creator_nickname=creator_nickname,
        creator_id=creator_id
    )
    db.add(taxi_pool)
    db.commit()
    return taxi_pool

def get_taxi_pool_id(db: Session, id: int):
    return db.query(TaxiPool).where(id == TaxiPool.id).first()

def select_taxi_pools_by_day(db: Session, start_date: datetime, end_date: datetime, order_time: bool = True):
    taxi_pools = db.query(TaxiPool).where(start_date < TaxiPool.start_time, TaxiPool.start_time < end_date).oredr_by(TaxiPool.start_time).all()
    return taxi_pools

def select_taxi_pools_by_id(db: Session, id: str):
    taxi_pool = db.query(TaxiPool).where(TaxiPool.id == id).first()
    return taxi_pool

def create_pool_member(db: Session, taxi_id:int, user_id:str):
    pool_member = PoolMember(
        taxi_id = taxi_id,
        user_id = user_id
    )
    db.add(pool_member)
    db.commit()
    return pool_member

def select_pool_member_by_taxi_user_id(db: Session, user_id:str, taxi_id:int):
    pool_member = db.query(PoolMember).where(PoolMember.user_id == user_id, PoolMember.taxi_id == taxi_id).first()
    return pool_member

def count_pool_members_by_taxi_id(db: Session, taxi_id: int):
    return db.query(PoolMember).filter(PoolMember.taxi_id == taxi_id).count()