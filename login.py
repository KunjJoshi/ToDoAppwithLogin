# models.py

from sqlalchemy import Column, Integer, Boolean, String
from database import Base

class Login(Base):
    __tablename__ = 'users'
    userid=Column(Integer,primary_key=True)
    username=Column(String(100),unique=True)
    password=Column(String(100))

    def __repr__(self):
        return '<Todo %r>' % (self.id)

