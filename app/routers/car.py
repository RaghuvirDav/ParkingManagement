"""
    Defines the API router for:
        - Add a new car
"""

from typing import Annotated

from fastapi import APIRouter, Depends
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


# create an employee
@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_car(db: db_dependency, car_request: CarRequest):
    car_model = Cars(**car_request.model_dump())
    db.add(car_model)
    db.commit()
