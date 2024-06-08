from model_settings import Base
from sqlalchemy import Column, Integer, String, Float, JSON

class User(Base):
    __tablename__ = 'User'
    user_tg_id = Column(Integer, primary_key=True)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    notifications_json = Column(JSON, nullable=True)
