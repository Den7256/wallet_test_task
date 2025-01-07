import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_balance():
    response = client.get("/api/v1/wallets/test-wallet-id")
    assert response.status_code == 404

def test_perform_operation_deposit():
    response = client.post("/api/v1/wallets/test-wallet-id/operation", json={"operationType": "DEPOSIT", "amount": 1000})
    assert response.status_code == 404  # Wallet not found

def test_perform_operation_withdraw():
    response = client.post("/api/v1/wallets/test-wallet-id/operation", json={"operationType": "WITHDRAW", "amount": 500})
    assert response.status_code == 404  # Wallet not found