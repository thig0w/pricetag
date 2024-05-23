# -*- coding: utf-8 -*-
import os
from time import sleep

from dotenv import load_dotenv

load_dotenv()
admin_name = os.environ.get("ADMIN_NAME")
admin_pass = os.environ.get("ADMIN_PASS")


def test_auth(client):
    # Fake user
    response = client.post(
        "http://127.0.0.1:8000/api/v1/users/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": "aaaaa",
            "password": "123",
        },
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}
    # True user
    response = client.post(
        "http://127.0.0.1:8000/api/v1/users/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": admin_name,
            "password": admin_pass,
        },
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"] is not None


def test_check_users_auth(client, token):
    response = client.get("http://127.0.0.1:8000/api/v1/users/")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

    response = client.get(
        "http://127.0.0.1:8000/api/v1/users/",
        headers={
            "accept": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
    assert response.status_code == 200
    assert response.json()[0].__contains__("username")


def test_check_users_me_auth(client, token):
    response = client.get("http://127.0.0.1:8000/api/v1/users/me/")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

    response = client.get(
        "http://127.0.0.1:8000/api/v1/users/me/",
        headers={
            "accept": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
    assert response.status_code == 200
    assert response.json()["username"] == admin_name


def test_check_users_param_auth(client, token):
    response = client.get(f"http://127.0.0.1:8000/api/v1/users/{admin_name}/")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

    response = client.get(
        f"http://127.0.0.1:8000/api/v1/users/{admin_name}/",
        headers={
            "accept": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
    assert response.status_code == 200
    assert response.json()["username"] == admin_name


def test_auth_expired_token(client, token):
    # wait until token is expired in dev env
    sleep(15)

    response = client.get(
        f"http://127.0.0.1:8000/api/v1/users/{admin_name}/",
        headers={
            "accept": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Token is expired"}
