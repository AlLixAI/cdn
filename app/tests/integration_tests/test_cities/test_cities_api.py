import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("city_name, true_city_name, status_code", [
    ("хабаровск", "", 400),
    ("Хабаровск", "", 400),
    ("Хабаровскфывфв", "",404),
    ("", "", 404),
    ("новая адыгея", "", 400),
    ("краснодар", "", 400),
    ("αθήνα", "", 400),
    ("Москва", "", 400),
    ("Новгород", "Городской Округ Великий Новгород", 201),
    ("новгород", "", 400),
    ("Ростов", "Ростов-На-Дону", 201),
    ("ростов", "", 400),
    ("ростов на дону", "", 400),
    ("ростов-на-дону", "", 400),
    ("ростов-на-дону ВоалдВЫОАЛДОАВОЫАЛДОДАЛОЫ", "", 404),
    ("ростов-на-дону ВоалдВЫОАЛДОАВОЫАЛДОДАЛОЫ", "", 404),
])
async def test_add_and_get_city1(city_name, true_city_name, status_code, ac: AsyncClient):
    response = await ac.post("/cities", params={
        "city_name": city_name
    })
    assert response.status_code == status_code
    if status_code == 201:
        assert response.json()["name"] == true_city_name


@pytest.mark.parametrize("city_name, nearest_city_name1, nearest_city_name2, status_code", [
    ("Краснодар", "Краснодар", "Новая Адыгея", 200),
    ("Новая Адыгея", "Новая Адыгея", "Краснодар", 200),
    ("Новая Адыгеяфывфвфывыфвфвфвфв", "Новая Адыгея", "Краснодар", 404),
    ("москва", "Москва", "Краснознаменск", 200),
    ("москва     - ", "Москва", "Краснознаменск", 200),
    ("", "", "", 404),
    ("Moscow", "Москва", "Краснознаменск", 200),
    ("moscow", "Москва", "Краснознаменск", 200),
    ("moscow                     ", "Москва", "Краснознаменск", 200),
    ("Krasnoznamensk", "Краснознаменск", "Москва", 200),
    ("               krasnoznamensk", "Краснознаменск", "Москва", 200),
])
async def test_add_and_get_city(city_name, nearest_city_name1, nearest_city_name2, status_code, ac: AsyncClient):
    response = await ac.get("/cities/nearest_cities_by_name", params={"city_name": city_name})
    assert response.status_code == status_code
    if status_code == 200:
        assert response.json()[0]["name"] == nearest_city_name1
        assert response.json()[1]["name"] == nearest_city_name2


@pytest.mark.parametrize("latitude, longitude, nearest_city_name1, nearest_city_name2, status_code", [
    (45.0351532, 38.9772396, "Краснодар", "Новая Адыгея", 200),
    (45.0247666, 38.9331639, "Новая Адыгея", "Краснодар", 200),
    (55.625578, 37.6063916, "Москва", "Краснознаменск", 200),
    (0.0, 0.0, "Αθήνα", "Hamburg", 200),
    (37.9755648, 23.7348324, "Αθήνα", "Новая Адыгея", 200),
    (38.9755648, 23.7348324, "Αθήνα", "Новая Адыгея", 200),
])
async def test_get_nearest_cities(latitude, longitude, nearest_city_name1, nearest_city_name2, status_code,
                                  ac: AsyncClient):
    response = await ac.get("/cities/nearest_cities_by_coord", params={"latitude": latitude, "longitude": longitude})
    assert response.status_code == status_code
    if status_code == 200:
        assert response.json()[0]["name"] == nearest_city_name1
        assert response.json()[1]["name"] == nearest_city_name2


@pytest.mark.parametrize("city_name, status_code", [
    ("Краснодар", 204),
    ("Krasnodar", 404),
    ("Новая Адыгея", 204),
    ("москва", 204),
    ("Хабаровск", 204),
    ("Несуществующий город", 404),
    (123, 404),
])
async def test_delete_city(city_name, status_code, ac: AsyncClient):
    response = await ac.delete(f"/cities/{city_name}/")
    assert response.status_code == status_code

    if status_code == 204:
        response = await ac.get(f"/cities/{city_name}/")
        assert response.status_code == 404
