from pydantic import BaseModel
from uuid import UUID


class CityResponse(BaseModel):
    id: UUID
    name: str
    latitude: float
    longitude: float

    @staticmethod
    def from_city(city):
        return CityResponse(
            id=city.id,
            name=city.name.title(),
            latitude=city.latitude,
            longitude=city.longitude
        )
