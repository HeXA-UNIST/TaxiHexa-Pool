import pytest
import json
import sys, os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from app import app

app_url = "http://localhost:8081"

# api settings
@pytest.fixture
def client():
    client = app.test_client()
    return client

# test /status
def test_status0(client):
    print(21372)
    resp = client.get(
        app_url+"/status"
    )
    print("resp", resp.data)
    assert resp.status_code == 200


# test /api/taxi_info/create
def test_create_group(client):
    data = {
        "start_position" : "2차 기숙사 앞",
        "end_position" : "울산역",
        "total_people" : 4,
        "start_time" : datetime.now()
    }
    resp = client.post(
        app_url+"/api/taxi_info/create",
        json=json.dumps(data)
    )

    assert resp.status_code == 200
    print(resp.data)

# test /api/taxi_info
def test_status2(client):
    data = {
        "start_position" : "2차 기숙사 앞",
        "end_position" : "울산역",
        "total_people" : 4,
        "start_time" : datetime.now()
    }
    resp = client.get(
        app_url+"/api/taxi_info/create",
        json=json.dumps(data)
    )
    print(11)
    assert resp.status_code == 200
    print(resp)
