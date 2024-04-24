"""
    This file starts the application.
    Creates an instance of FastAPI().
    And a /healthy endpoint to check health of the application.
"""
from fastapi import FastAPI
from .models import Base
from .database import engine
from .routers import car, employee

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(car.router)
app.include_router(employee.router)


# Health check endpoint
@app.get("/healthy/")
def health_check():
    return {"status": "Healthy"}
