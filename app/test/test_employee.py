"""
    Tests API endpoint for health
    -   POST - /emp
"""
from starlette import status

from .utils import *
from ..routers.employee import get_db

app.dependency_overrides[get_db] = override_get_db


def test_add_emp(test_emp):
    request_data = {'name': 'Another User', 'is_active': True, 'id': 1}

    response = client.post("/emp", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Employees).filter(Employees.id == 2).first()

    assert model.name == request_data.get("name")
