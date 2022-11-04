from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from pathlib import Path
import sys

path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path + "/fastapi_app")
from app import app, get_db
from models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_add_a_rating(test_db):
    response = client.post(
        "/",
        json={
            "id_trip": "trip10",
            "id_user_scorer": "user_scorer",
            "id_user_scored": "user_scored",
            "value": 3,
        },
    )
    assert response.status_code == 200

    response = client.get("/user_scorer")
    assert response.status_code == 200
    data = response.json()[0]
    assert data["id_trip"] == "trip10"
    assert data["id_user_scored"] == "user_scored"
    assert data["value"] == 3


def test_add_two_ratings_with_same_trip_id(test_db):
    response = client.post(
        "/",
        json={
            "id_trip": "trip10",
            "id_user_scorer": "user_scorer",
            "id_user_scored": "user_scored",
            "value": 3,
        },
    )
    assert response.status_code == 200

    response = client.post(
        "/",
        json={
            "id_trip": "trip10",
            "id_user_scorer": "other",
            "id_user_scored": "not me",
            "value": 5,
        },
    )
    assert response.status_code == 400


def test_a_user_cant_rate_himself(test_db):
    response = client.post(
        "/",
        json={
            "id_trip": "bestTripEver",
            "id_user_scorer": "me",
            "id_user_scored": "me",
            "value": 1,
        },
    )
    assert response.status_code == 400


def test_average_of_one_rating(test_db):
    response = client.post(
        "/",
        json={
            "id_trip": "trip10",
            "id_user_scorer": "user_scorer",
            "id_user_scored": "user_scored",
            "value": 2,
        },
    )
    assert response.status_code == 200

    response = client.get("/user_scored/average")
    assert response.status_code == 200
    data = response.json()
    assert data == 2


def test_average_of_two_ratings(test_db):
    response = client.post(
        "/",
        json={
            "id_trip": "trip10",
            "id_user_scorer": "user_scorer",
            "id_user_scored": "user_scored",
            "value": 3,
        },
    )
    assert response.status_code == 200

    response = client.post(
        "/",
        json={
            "id_trip": "trip110",
            "id_user_scorer": "user_scorer",
            "id_user_scored": "user_scored",
            "value": 5,
        },
    )
    assert response.status_code == 200

    response = client.get("/user_scored/average")
    assert response.status_code == 200
    data = response.json()
    assert data == 4


def test_average_of_invalid_user(test_db):
    response = client.get("/user_scored/average")
    assert response.status_code == 404
