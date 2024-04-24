"""
    Tests API endpoint for health
    -   GET - /healthy
"""
from fastapi import status
from .utils import *


def test_run_health_check():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "Healthy"}
