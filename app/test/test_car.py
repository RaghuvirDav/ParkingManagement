"""
    Tests API endpoint for car
    -   POST - /car
"""
from starlette import status

from .utils import *
from ..routers.car import get_db

app.dependency_overrides[get_db] = override_get_db


def test_add_car(test_car):
    request_data = {
        'color': 'Black',
        'make': 'Toyota',
        'model': 'Prius',
        'number_plate': 'AS98 GHJ'
    }

    response = client.post("/car", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Cars).filter(Cars.id == 2).first()

    assert model.make == request_data.get("make")
    assert model.model == request_data.get("model")
    assert model.color == request_data.get("color")
    assert model.number_plate == request_data.get("number_plate")


def test_get_all_cars(test_car):
    response = client.get("/car")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {'color': 'White', 'id': 1, 'owner_id': None, 'make': 'Toyota', 'model': 'Fortuner', 'number_plate': 'ZX10 MNB'}
    ]


def test_get_all_cars_not_found():
    response = client.get("/car")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': "No cars found."}
