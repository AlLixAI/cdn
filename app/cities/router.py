from typing import Optional

from fastapi import APIRouter, status, Depends, HTTPException, Query
from fastapi_cache.decorator import cache
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.cities.dao import CitiesDAO
from app.cities.schemas import CityResponse
from app.cities.utils import get_coordinates
from app.database import get_async_session
from app.exceptions import CityNotFound, CityAlreadyExist, CitiesNotFound
from app.service.cache import clear_cache

router = APIRouter(
    prefix="/cities",
    tags=["cities"]
)


@router.get(
    "",
    response_model=list[CityResponse],
    summary="Получение доступных городов-узлов",
    description="Эндпоинт получения доступных городов-узлов"
)
@cache()
async def get_cities(
        limit: Optional[int] = Query(None, ge=1),
        offset: Optional[int] = Query(0, ge=0)
):
    try:
        # Получаем все города из базы данных
        cities = await CitiesDAO.find_all(limit, offset)

        return [CityResponse.from_city(city) for city in cities]

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


@router.get(
    "/{city_name}/",
    response_model=CityResponse,
    summary="Получения данных по конкретному городу-узлу по названию",
    description="Эндпоинт получения данных по конкретному городу-узлу по названию"
)
@cache()
async def get_city(
        city_name: str,
):
    try:
        true_city_name = await get_coordinates(city_name)
        city_name = true_city_name['name']
        # Получаем город по имени
        city = await CitiesDAO.find_one_or_none(name=city_name.lower())
        if city is None:
            raise CityNotFound

        return CityResponse.from_city(city)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CityResponse,
    summary="Добавление нового города-узла",
    description="Эндпоинт для добавления нового города-узла"
)
async def create_city(
        city_name: str,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        # Получаем координаты города
        coordinates = await get_coordinates(city_name)

        # Проверяем, были ли получены координаты
        if 'error' in coordinates:
            raise HTTPException(status_code=400, detail=coordinates['error'])

        new_city = await CitiesDAO.add(coordinates['name'], coordinates, session)

        await clear_cache()

        return CityResponse.from_city(new_city)

    except IntegrityError as _:
        await session.rollback()
        raise CityAlreadyExist(f"'{coordinates['name']}' ('{city_name}')")
    except HTTPException as e:
        await session.rollback()
        raise e
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete(
    "/{city_name}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление города-узла",
    description="Эндпоинт для удаления города-узла"
)
async def delete_city(
        city_name: str,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        true_city_name = await get_coordinates(city_name)
        city_name = true_city_name['name']
        # Ищем город по имени
        city = await CitiesDAO.find_one_or_none(name=city_name.lower())
        if city is None:
            raise CityNotFound

        await session.delete(city)
        await session.commit()
        await clear_cache()

    except HTTPException as e:
        await session.rollback()
        raise e
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
    "/nearest_cities_by_coord",
    response_model=list[CityResponse],
    summary="Поиск ближайшего города-узла по координатам",
    description="Эндпоинт для поиск ближайшего города-узла по координатам"
)
@cache()
async def get_nearest_cities(
        latitude: float,
        longitude: float,
        limit: int = Query(2, ge=1),
        offset: Optional[int] = Query(0, ge=0),
):
    try:
        nearest_cities = await CitiesDAO.find_nearest_by_coord(
            latitude=latitude,
            longitude=longitude,
            limit=limit,
            offset=offset)
        if not nearest_cities:
            raise CitiesNotFound

        return [CityResponse.from_city(city) for city in nearest_cities]

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
    "/nearest_cities_by_name",
    response_model=list[CityResponse],
    summary="Поиск ближайшего города-узла по названию",
    description="Эндпоинт для поиск ближайшего города-узла по названию"
)
@cache()
async def get_nearest_cities_by_name(
        city_name: str,
        limit: int = Query(2, ge=1),
        offset: Optional[int] = Query(0, ge=0),
):
    try:
        nearest_cities = await CitiesDAO.find_nearest_by_name(
            city_name=city_name,
            limit=limit,
            offset=offset
        )
        if not nearest_cities:
            raise CitiesNotFound

        return [CityResponse.from_city(city) for city in nearest_cities]

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
