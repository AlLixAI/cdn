import aiohttp

from app.exceptions import CityNotFound, APIError


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
                        'name': data[0]['name'],
                        'latitude': data[0]['lat'],
                        'longitude': data[0]['lon']
                    }
                else:
                    raise CityNotFound
            else:
                raise APIError
