import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from fast_bloge.models.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)


class UserIP(Base):
    __tablename__ = 'IP'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    ip = Column(String)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)


