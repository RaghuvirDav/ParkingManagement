"""
    Tests API endpoint for car
    -   POST - /car - Add a new employee
    -   GET - /car - Get all cars
    -   GET - /car/{car_make} - Filter cars by "car_make"
    -   PUT - /car/{car_id} - Update Car
    -   DELETE - /car/{car_id} - Delete Car

    -   PUT - /car/register/{number_plate} - Add car to an employee
    -   GET - /car/register/ - GET all registered Cars with employees
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


def test_get_car_by_make(test_car):
    response = client.get("/car/Toyota")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {'color': 'White', 'id': 1, 'owner_id': None, 'make': 'Toyota', 'model': 'Fortuner', 'number_plate': 'ZX10 MNB'}
    ]


def test_get_car_by_make_not_found():
    response = client.get("/car/unknown_make")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': "No cars found."}


def test_update_car(test_car):
    request_data = {
        'color': 'Black',
        'make': 'Toyota',
        'model': 'Fortuner',
        'number_plate': 'ZX10 MNB'
    }

    response = client.put("/car/1", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Cars).filter(Cars.id == 1).first()

    assert model.color == "Black"


def test_update_car_not_found(test_car):
    request_data = {
        'color': 'Black',
        'make': 'Toyota',
        'model': 'Fortuner',
        'number_plate': 'ZX10 MNB'
    }

    response = client.put("/car/1000", json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': "Car not found."}


def test_delete_car(test_car):
    response = client.delete("/car/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Cars).filter(Cars.id == 1).first()
    assert model is None


def test_delete_car_not_found():
    response = client.delete("/car/1000")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': "Car not found."}


def test_add_car_to_employee(test_car, test_emp):
    request_data = {
        'color': 'White',
        'owner_id': test_emp.id,
        'make': 'Toyota',
        'model': 'Fortuner',
        'number_plate': 'ZX10 MNB'
    }

    response = client.put("/car/register/ZX10 MNB", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Cars).filter(Cars.id == 1).first()

    assert model.owner_id == 1


def test_add_car_to_employee_car_not_found(test_car, test_emp):
    request_data = {
        'color': 'Black',
        'owner_id': test_emp.id,
        'make': 'Toyota',
        'model': 'Fortuner',
        'number_plate': 'ZX10 MNB'
    }

    response = client.put("/car/register/ZX10 MNA", json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': "Car not found."}


def test_add_car_to_employee_emp_not_found(test_car, test_emp):
    request_data = {
        'color': 'Black',
        'owner_id': 2,
        'make': 'Toyota',
        'model': 'Fortuner',
        'number_plate': 'ZX10 MNB'
    }

    response = client.put("/car/register/ZX10 MNB", json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': "Employee not found."}


def test_get_registered_cars(test_register_car_to_emp):
    response = client.get("/car/register/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            'id': 1,
            'make': 'Toyota',
            'color': 'White',
            'model': 'Fortuner',
            'owner_id': 1,
            'number_plate': 'ZX10 MNB',
            'name': 'User Name'
        }
    ]


def test_get_registered_cars_not_found():
    response = client.get("/car/register/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': "No cars found."}


