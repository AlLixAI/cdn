import pytest

from app.cities.dao import CitiesDAO

@pytest.mark.parametrize("name, exist",[
    ("казань", True),
    ("Казань", False),
    ("лалаленд", False),
    ("αθήνα", True),
    ("", False),
])
async def test_find_city_one_or_none(name, exist):
    city = await CitiesDAO.find_one_or_none(name=name)

    if exist:
        assert city
        assert city.name == name
    else:
        assert not city

@pytest.mark.parametrize("exist",[
    (True),
])
async def test_find_all_city(exist):
    cities = await CitiesDAO.find_all()

    if exist:
        assert isinstance(cities, list)
        assert len(cities) > 0
    else:
        assert not cities

@pytest.mark.parametrize("latitude, longitude, exist",[
    (0, 0, True),
    (1, 1, True),
    (1000, 1000, True),
    (1000000000, 100000000000, True),
    (999999999999999, 99999999999, True),
    (-10000000000000, 0, True),
    (-999999999999999999, -9999999999999999, True)
])
async def test_find_nearest_by_coord(latitude, longitude, exist):
    cities = await CitiesDAO.find_nearest_by_coord(latitude, longitude)

    if exist:
        assert isinstance(cities, list)
        assert len(cities) > 0
    else:
        assert not cities