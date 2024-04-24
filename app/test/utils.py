"""
    Creates a local DB for testing.
    Configurations for Test DB.
    override_get_db method to override get_db method and point to test DB.
    fixtures to create emp and car records to test db.
"""
import pytest
from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from ..database import Base
from ..main import app
from ..models import Cars, Employees

SQLALCHEMY_DATABASE_URL = "sqlite:///./parking_management_app_test_db.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


client = TestClient(app)


@pytest.fixture()
def test_car():
    car = Cars(
        make="Toyota",
        model="Fortuner",
        color="White",
        number_plate="ZX10 MNB",
    )

    db = TestingSessionLocal()
    db.add(car)
    db.commit()

    yield car
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM cars;"))
        connection.commit()


@pytest.fixture()
def test_emp():
    emp = Employees(
        name="User Name",
    )

    db = TestingSessionLocal()
    db.add(emp)
    db.commit()

    yield emp
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM employees;"))
        connection.commit()


@pytest.fixture()
def test_register_car_to_emp(test_car, test_emp):
    request_data = {
        'color': 'White',
        'owner_id': test_emp.id,
        'make': 'Toyota',
        'model': 'Fortuner',
        'number_plate': 'ZX10 MNB'
    }

    client.put("/car/register/ZX10 MNB", json=request_data)

