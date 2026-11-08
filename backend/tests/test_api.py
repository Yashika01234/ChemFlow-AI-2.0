from fastapi.testclient import TestClient
from app.main import app
from app.db import init_db

init_db()
client = TestClient(app)

def test_health():
    assert client.get("/health").json()["status"] == "healthy"

def test_compound_endpoint():
    response = client.post("/api/compounds/analyze", json={"smiles": "CCO", "name": "ethanol"})
    assert response.status_code == 200
    assert response.json()["formula"] == "C2H6O"

def test_balance_endpoint():
    response = client.post("/api/stoichiometry/balance", json={"equation": "H2 + O2 -> H2O"})
    assert response.status_code == 200
    assert response.json()["balanced_equation"] == "2H2 + O2 -> 2H2O"

def test_invalid_reaction():
    response = client.post("/api/reactions/predict", json={"reaction": "magic", "reactants": ["CCO"]})
    assert response.status_code == 422
