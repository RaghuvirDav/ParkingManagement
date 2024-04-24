"""
    Defines the API router for:
    -   POST - /car - Add a new employee
    -   GET - /car - Get all cars
    -   GET - /car/{car_make} - Filter cars by "car_make"
    -   PUT - /car/{car_id} - Update Car
    -   DELETE - /car/{car_id} - Delete Car
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from app.database import SessionLocal
from app.models import Cars

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