"""
    Describes the database schema.
    Describe Tables and its columns.
"""
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Employees(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class Cars(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String)
    model = Column(String)
    color = Column(String)
    number_plate = Column(String, unique=True)
    owner_id = Column(Integer, ForeignKey("employees.id"))
