from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.db import Base


class PostRaw(Base):
    __tablename__ = "posts_raw"

    id = Column(Integer, primary_key=True)
    source = Column(String)
    text = Column(Text)
    url = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    processed = Column(Boolean, default=False)


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True)
    text = Column(Text)
    lat = Column(String)
    lon = Column(String)
    source_url = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    status = Column(String, default="new")