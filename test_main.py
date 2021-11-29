from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_read_surveys():
  response = client.get("/")
  assert response.status_code == 200

def test_read_sightings():
  response = client.get("/sightings")
  assert response.status_code == 200

def test_read_sightings_id():
  response = client.get("/sightings/1")
  assert response.status_code == 404
  assert response.json () == {"detail" : "sighting not found"}