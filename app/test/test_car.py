"""
    Tests API endpoint for health
    -   POST - /car
"""
from starlette import status

from .utils import *
from ..routers.car import get_db

app.dependency_overrides[get_db] = override_get_db


def test_add_car():
    request_data = {
        'color': 'Black',
        'make': 'Toyota',
        'model': 'Prius',
        'number_plate': 'AS98 GHJ'
    }

    response = client.post("/car", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Cars).filter(Cars.id == 1).first()

    assert model.make == request_data.get("make")
    assert model.model == request_data.get("model")
    assert model.color == request_data.get("color")
    assert model.number_plate == request_data.get("number_plate")