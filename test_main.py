from fastapi import FastAPI
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_read_main():
    d = {
        "names": ["Jose", "Tere"],
        "tasks": ["lavar", "cocinar"],
        "days": ["Lunes", "Martes", "Miércoles"],
        "costs": {
            "Jose": {"lavar": 1, "cocinar": 1},
            "Tere": {"lavar": 1, "cocinar": 1},
        },
        "min_assign_task": 1,
        "max_assign_task": 7,
        "max_total_assign": 5,
        "min_total_assign": 1,
    }
    response = client.post("/resolve/", json=d)
    assert response.status_code == 200
    """ assert response.json() == {
        "assignation": {
            "lavar": {
                "Lunes": "Jose",
                "Martes": "Jose",
                "Miércoles": "Tere"
            },
            "cocinar": {
                "Lunes": "Tere",
                "Martes": "Tere",
                "Miércoles": "Jose"
            }
        },
        "status": "Optimal",
        "value": 6,
        "names": [
            "Jose",
            "Tere"
        ],
        "tasks": [
            "lavar",
            "cocinar"
        ],
        "days": [
            "Lunes",
            "Martes",
            "Miércoles"
        ],
        "costs": {
            "Jose": {
                "lavar": 1,
                "cocinar": 1
            },
            "Tere": {
                "lavar": 1,
                "cocinar": 1
            }
        },
        "min_assign_task": 1,
        "max_assign_task": 7,
        "min_total_assign": 1,
        "max_total_assign": 5
    }
 """
