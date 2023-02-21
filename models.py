# models.py

from sqlalchemy import Column, Integer, Boolean, String
from database import Base

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    task = Column(String(100))
    time=Column(String(100))
    completed = Column(Boolean, default=False)

    def __repr__(self):
        return '<Todo %r>' % (self.id)

