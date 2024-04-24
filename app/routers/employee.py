"""
    Defines the API router for:
    -   POST - /emp - Add a new employee
    -   GET - /emp - Get all employees

"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from app.database import SessionLocal
from app.models import Employees

router = APIRouter(
    prefix="/emp",
    tags=["Emp"]
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


class EmpRequest(BaseModel):
    """
        Defines code to validate create employee request against defined constrains
    """
    name: str = Field(min_length=2, default="Employee Name")


# create an employee
@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_emp(db: db_dependency, emp_request: EmpRequest):
    emp_model = Employees(**emp_request.model_dump())
    db.add(emp_model)
    db.commit()


# get all employees
@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_employees(db: db_dependency):
    emp_list = db.query(Employees).all()
    if len(emp_list) > 0:
        return emp_list
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No employees found.")
