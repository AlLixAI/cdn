from fastapi import HTTPException
from geoalchemy2.functions import ST_SetSRID, ST_MakePoint, ST_DistanceSphere
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.cities.utils import get_coordinates
from app.service.base_dao import BaseDAO
from app.cities.models import City


class CitiesDAO(BaseDAO):
    model = City

    @classmethod
    async def add(cls, name, coordinates, session: AsyncSession):
        new_city = cls.model(
            name=name.lower(),
            geom=f'SRID=4326;POINT({coordinates["longitude"]} {coordinates["latitude"]})',
            latitude=float(coordinates["latitude"]),
            longitude=float(coordinates["longitude"])
        )

        session.add(new_city)

        await session.commit()
        await session.refresh(new_city)
        new_city.name = new_city.name.title()
        return new_city

    @classmethod
    async def find_nearest_by_coord(cls, latitude, longitude, session: AsyncSession, limit=2, offset=0):
        point = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)
        result = await session.execute(
            select(cls.model)
            .order_by(ST_DistanceSphere(cls.model.geom, point))
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all()

    @classmethod
    async def find_nearest_by_name(cls, city_name, session: AsyncSession, limit=2, offset=0):
        coordinates = await get_coordinates(city_name)

        if not coordinates:
            raise HTTPException(status_code=404, detail="Город не найден")

        result = await cls.find_nearest_by_coord(
            latitude=float(coordinates["latitude"]),
            longitude=float(coordinates["longitude"]),
            session=session,
            limit=limit,
            offset=offset
        )
        return result
