"""
    Tests API endpoint for employee
    -   POST - /emp
    -   GET - /emp
"""
from starlette import status

from .utils import *
from ..routers.employee import get_db

app.dependency_overrides[get_db] = override_get_db


def test_add_emp(test_emp):
    request_data = {'name': 'Another User', 'id': 1}

    response = client.post("/emp", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Employees).filter(Employees.id == 2).first()

    assert model.name == request_data.get("name")


def test_get_all_employees(test_emp):
    response = client.get("/emp")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {'name': 'User Name', 'id': 1}
    ]


def test_get_all_cars_not_found():
    response = client.get("/emp")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': "No employees found."}
