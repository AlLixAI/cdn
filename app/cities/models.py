from geoalchemy2 import Geometry
from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database import Base


class City(Base):
    __tablename__ = 'cities'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, unique=True, nullable=False)
    name = Column(String(length=200), nullable=False, index=True, unique=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    geom = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
