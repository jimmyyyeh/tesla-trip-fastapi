# -*- coding: utf-8 -*
"""
      ┏┓       ┏┓
    ┏━┛┻━━━━━━━┛┻━┓
    ┃      ☃      ┃
    ┃  ┳┛     ┗┳  ┃
    ┃      ┻      ┃
    ┗━┓         ┏━┛
      ┗┳        ┗━┓
       ┃          ┣┓
       ┃          ┏┛
       ┗┓┓┏━━━━┳┓┏┛
        ┃┫┫    ┃┫┫
        ┗┻┛    ┗┻┛
    God Bless,Never Bug
"""
from datetime import datetime
from random import choice
from typing import List

from fastapi.testclient import TestClient
from pytest_mock.plugin import MockerFixture

from app import create_app
from database.models import CarModel
from routes import car
from utils.response_models import Response, Car

app = create_app()
app.include_router(car.router)

client = TestClient(app)


class TestCar:

    @staticmethod
    def _get_car_model(car_info: dict):
        car_model = CarModel(
            id=1,
            model=car_info['model'],
            spec=car_info['spec']
        )
        return car_model

    @staticmethod
    def _get_cars():
        models = ['Model 3', 'Model S', 'Model X']
        specs = ['Long Range', 'Standard']
        date_ = datetime.now().date()
        cars = list()
        for i in range(5):
            car_ = Car(
                id=i + 1,
                model=choice(models),
                spec=choice(specs),
                has_image=choice([True, False]),
                manufacture_date=date_
            )
            cars.append(car_)
        return cars

    def test_create_car(self, mocker: MockerFixture, car_info: dict):
        mocker.patch('database.db_handler.DBHandler.get_car_models',
                     return_value=self._get_car_model(car_info=car_info))
        payload = car_info
        payload.update({'manufacture_date': datetime.now().strftime('%Y-%m-%d')})
        response = client.post('/cars', json=payload, headers={})
        assert response.status_code == 200
        assert Response[Car].validate(response.json())

    def test_update_car(self, mocker: MockerFixture, car_info: dict):
        ...

    def test_get_single_car(self, mocker: MockerFixture):
        mocker.patch('database.db_handler.DBHandler.get_cars', return_value=self._get_cars())
        response = client.get('/cars/1', headers={})
        assert response.status_code == 200
        assert Response[Car].validate(response.json())

    def test_get_cars(self, mocker: MockerFixture):
        mocker.patch('database.db_handler.DBHandler.get_cars', return_value=self._get_cars())
        response = client.get('/cars', headers={})
        assert response.status_code == 200
        assert Response[List[Car]].validate(response.json())

    def test_delete_car(self):
        ...
