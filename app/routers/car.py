"""
    Defines the API router for:
    -   POST - /car - Add a new employee
    -   GET - /car - Get all cars
    -   GET - /car/{car_make} - Filter cars by "car_make"
    -   PUT - /car/{car_id} - Update Car
    -   DELETE - /car/{car_id} - Delete Car

    -   PUT - /car/register/{number_plate} - Add car to an employee
    -   GET - /car/register/ - GET all registered Cars with employees
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from app.database import SessionLocal
from app.models import Cars, Employees

router = APIRouter(
    prefix="/car",
    tags=["Car"]
)


# creates and maintains a DB session until all DB operations are completed
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# create a new DB connection
db_dependency = Annotated[Session, Depends(get_db)]


class CarRequest(BaseModel):
    """
            Defines code to validate create car request against defined constrains
    """
    make: str = Field(min_length=2, default="Toyota")
    model: str = Field(min_length=1, default="Yaris")
    color: str = Field(min_length=2, default="White")
    number_plate: str = Field(max_length=8, min_length=8, default="AB01 DEF")


class AddCarRequest(BaseModel):
    """
                Defines code to validate add_car_to_emp request against defined constrains
    """
    number_plate: str = Field(max_length=8, min_length=8, default="AB01 DEF")
    owner_id: int = Field(gt=0, default=1)


# create a car
@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_car(db: db_dependency, car_request: CarRequest):
    car_model = Cars(**car_request.model_dump())
    db.add(car_model)
    db.commit()


# Get all cars
@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_cars(db: db_dependency):
    car_list = db.query(Cars).all()
    if len(car_list) > 0:
        return car_list
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No cars found.")


# get(Filter) cars my make
@router.get("/{car_make}", status_code=status.HTTP_200_OK)
async def get_car_by_make(db: db_dependency, car_make: str):
    car_model = db.query(Cars).filter(Cars.make == car_make).all()
    if len(car_model) > 0:
        return car_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No cars found.")


# Update car
@router.put("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_car(db: db_dependency,
                     car_request: CarRequest,
                     car_id: int = Path(gt=0)):
    car_model = db.query(Cars).filter(Cars.id == car_id).first()
    if car_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found.")

    car_model.make = car_request.make
    car_model.model = car_request.model
    car_model.color = car_request.color

    db.add(car_model)
    db.commit()


# Delete a car
@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car(db: db_dependency, car_id: int = Path(gt=0)):
    car_model = db.query(Cars).filter(Cars.id == car_id).first()
    if car_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found.")

    db.query(Cars).filter(Cars.id == car_id).delete()
    db.commit()


# ADD a car to Employee
@router.put("/register/{number_plate}", status_code=status.HTTP_201_CREATED)
async def add_car_to_employee(db: db_dependency, add_car_request: AddCarRequest, number_plate: str):
    car_model = db.query(Cars).filter(Cars.number_plate == number_plate).first()
    if car_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found.")

    emp_model = db.query(Employees).filter(Employees.id == add_car_request.owner_id).first()
    if emp_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found.")

    car_model.owner_id = add_car_request.owner_id

    db.add(car_model)
    db.commit()


# Get all registered cars
@router.get("/register/", status_code=status.HTTP_200_OK)
async def get_registered_cars(db: db_dependency):
    car_list = db.query(Cars.id, Cars.make, Cars.color, Cars.model, Cars.owner_id, Cars.number_plate, Employees.id,
                        Employees.name).filter(Cars.owner_id is not None).join(Employees,
                                                                               Cars.owner_id == Employees.id).all()

    car_list1 = db.query(Cars).all()
    if len(car_list) > 0:
        b = []
        for i in car_list:
            b.append(i._asdict())
        return b
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No cars found.")