from .database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime


class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    body = Column(Text)
    published = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
