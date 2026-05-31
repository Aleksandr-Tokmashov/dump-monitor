from app.db import Base
from sqlalchemy import Column, Integer, String, Float


class RailwayStation(Base):
    __tablename__ = "railway_stations"

    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True, nullable=False)

    lat = Column(Float)
    lon = Column(Float)