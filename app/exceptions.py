from fastapi import HTTPException


class CitiesException(HTTPException):
    status_code = 500
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class CitiesNotFound(CitiesException):
    status_code = 404
    detail = "Городов не найдено"


class CityNotFound(CitiesException):
    status_code = 404
    detail = "Город не найден"


class CityAlreadyExist(CitiesException):
    status_code = 400

    def __init__(self, city_name):
        self.detail = f"Город с именем {city_name} уже существует"
        super().__init__()


class APIError(HTTPException):
    status_code = 502
    detail = "Проблемы с внешним API"
