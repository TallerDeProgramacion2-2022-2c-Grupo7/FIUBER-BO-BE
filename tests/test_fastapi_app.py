from fastapi.testclient import TestClient

from pathlib import Path
import sys
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path + "/fastapi_app")

from app import app

client = TestClient(app)

def test_hola_mundo():
    response = client.get("/hola")
    assert response.status_code == 200
    assert response.json() == "Hola mundo!"
