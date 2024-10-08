import aiohttp
from fastapi import HTTPException


async def get_coordinates(
        location: str,
        format_response: str = 'json',
        limit: int = 1
) -> dict:
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': location,
        'format': format_response,
        'limit': limit
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                if data:
                    return {
                        'latitude': data[0]['lat'],
                        'longitude': data[0]['lon']
                    }
                else:
                    raise HTTPException(status_code=404, detail="Город не найден")
            else:
                raise HTTPException(status_code=502, detail="Проблемы с внешним API")
