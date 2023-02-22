# -*- coding: utf-8 -*-
import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

from src.pricetag import create_app

load_dotenv()
admin_name = os.environ.get("ADMIN_NAME")
admin_pass = os.environ.get("ADMIN_PASS")


@pytest.fixture
def client():
    app = create_app()
    client = TestClient(app)
    return client


@pytest.fixture
def token(client):
    response = client.post(
        "http://127.0.0.1:8000/api/v1/users/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": admin_name,
            "password": admin_pass,
        },
    )
    return response.json()["access_token"]
