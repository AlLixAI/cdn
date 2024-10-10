from fastapi import HTTPException
from geoalchemy2.functions import ST_SetSRID, ST_MakePoint, ST_DistanceSphere
from sqlalchemy import select, delete

from app.cities.utils import get_coordinates
from app.database import async_session_maker
from app.service.base_dao import BaseDAO
from app.cities.models import City


class CitiesDAO(BaseDAO):
    model = City

    @classmethod
    async def add(cls, city_name, coordinates):
        async with async_session_maker() as session:

            async with session.begin():
                new_city = cls.model(
                    name=city_name.lower(),
                    geom=f'SRID=4326;POINT({coordinates["longitude"]} {coordinates["latitude"]})',
                    latitude=float(coordinates["latitude"]),
                    longitude=float(coordinates["longitude"])
                )

                session.add(new_city)

            await session.refresh(new_city)

            new_city.name = new_city.name.title()
            return new_city

    @classmethod
    async def find_nearest_by_coord(cls, latitude, longitude, limit=2, offset=0):
        async with async_session_maker() as session:
            point = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)
            result = await session.execute(
                select(cls.model)
                .order_by(ST_DistanceSphere(cls.model.geom, point))
                .offset(offset)
                .limit(limit)
            )
            return result.scalars().all()

    @classmethod
    async def find_nearest_by_name(cls, city_name, limit=2, offset=0):
        coordinates = await get_coordinates(city_name)

        if not coordinates:
            raise HTTPException(status_code=404, detail="Город не найден")

        result = await cls.find_nearest_by_coord(
            latitude=float(coordinates["latitude"]),
            longitude=float(coordinates["longitude"]),
            limit=limit,
            offset=offset
        )
        return result


    @classmethod
    async def delete_by_name(cls, city_name):
        async with async_session_maker() as session:
            async with session.begin():
                await session.execute(
                    delete(cls.model).where(cls.model.name == city_name.lower())
                )
                await session.commit()