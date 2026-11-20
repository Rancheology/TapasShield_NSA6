"""
TapasShield End-to-End REST & WebSocket API Integration Tests (NSA 6.0).
Verifies full FastAPI server lifecycle, scenario injection, and inspector audit endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_api_status_endpoint(client):
    """Verifies GET /api/status returns valid telemetry, physics, and crypto fields."""
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert "telemetry" in data
    assert "raw_physics" in data
    assert "cryptography" in data
    assert "diagnostics" in data
    assert data["telemetry"]["boiler_id"] == "IBR-TN-VEL-2026-0891"


def test_api_public_key_endpoint(client):
    """Verifies GET /api/public-key returns NIST P-256 PEM."""
    response = client.get("/api/public-key")
    assert response.status_code == 200
    data = response.json()
    assert data["algorithm"] == "ECDSA_NIST_P256"
    assert data["curve"] == "secp256r1"
    assert "-----BEGIN PUBLIC KEY-----" in data["public_key_pem"]


def test_api_scenario_injection(client):
    """Verifies triggering scenarios 1 through 5 via REST API."""
    # Scenario 1: Normal
    r1 = client.post("/api/scenario/1")
    assert r1.status_code == 200
    assert r1.json()["status"] == "RESET_NORMAL"

    # Scenario 2: Scale buildup
    r2 = client.post("/api/scenario/2")
    assert r2.status_code == 200
    assert r2.json()["status"] == "SCALE_BUILDUP_ACTIVE"

    # Scenario 3: Overpressure
    r3 = client.post("/api/scenario/3")
    assert r3.status_code == 200
    assert r3.json()["status"] == "MAWP_EMERGENCY_ACTIVE"

    # Scenario 4: Wire cut
    r4 = client.post("/api/scenario/4")
    assert r4.status_code == 200
    assert r4.json()["status"] == "WIRE_CUT_ACTIVE"

    # Scenario 5: Resistor spoof & DB tamper
    r5 = client.post("/api/scenario/5")
    assert r5.status_code == 200
    assert r5.json()["status"] == "RESISTOR_SPOOF_AND_DB_TAMPER_ACTIVE"


def test_api_ledger_and_audit(client):
    """Verifies ledger records retrieval and statutory audit scan."""
    # Reset system first
    client.post("/api/reset")

    ledger_res = client.get("/api/ledger?count=10")
    assert ledger_res.status_code == 200
    records = ledger_res.json()["records"]
    assert len(records) > 0

    # Initial audit should be 100% valid
    audit_res = client.get("/api/ledger/audit")
    assert audit_res.status_code == 200
    assert audit_res.json()["chain_valid"] is True


def test_api_db_tamper_and_forensic_detection(client):
    """Verifies that simulating DB tamper is immediately caught by the audit scan."""
    # Inject database tamper
    tamper_res = client.post("/api/simulate/db-tamper")
    assert tamper_res.status_code == 200
    tamper_data = tamper_res.json()
    assert tamper_data["success"] is True

    # Audit scan must catch the fraud
    audit_res = client.get("/api/ledger/audit")
    assert audit_res.status_code == 200
    audit_data = audit_res.json()
    assert audit_data["chain_valid"] is False
    assert audit_data["tampered_block_seq"] == tamper_data["tampered_seq_no"]


def test_frontend_static_serving(client):
    """Verifies that the compiled production React frontend is served at /."""
    response = client.get("/")
    assert response.status_code == 200
    assert "<!doctype html>" in response.text.lower()
    assert "TapasShield" in response.text


def test_api_eodb_endpoints(client):
    """Verifies EODB National Cluster Grid and IBR Form-VI Digital Certificate generation and revocation."""
    # Reset system first to clean state
    client.post("/api/reset")

    # 1. Test National Registry Endpoint
    reg_res = client.get("/api/eodb/national-registry")
    assert reg_res.status_code == 200
    reg_data = reg_res.json()
    assert "boilers" in reg_data
    boilers = reg_data["boilers"]
    assert len(boilers) >= 5
    boiler_ids = [b["registration_id"] for b in boilers]
    assert "IBR-TN-VEL-2026-0891" in boiler_ids
    assert any("Tiruppur" in b["cluster_name"] for b in boilers)
    assert any("Surat" in b["cluster_name"] for b in boilers)
    assert any("Pune" in b["cluster_name"] for b in boilers)
    assert any("Ludhiana" in b["cluster_name"] for b in boilers)
    assert "14 Days" in reg_data.get("summary", {}).get("eodb_delay_reduction", "")

    # 2. Test Certificate in clean state
    cert_res = client.get("/api/eodb/certificate")
    assert cert_res.status_code == 200
    cert = cert_res.json()
    assert cert["boiler_registration_id"] == "IBR-TN-VEL-2026-0891"
    assert "Tamil Nadu" in cert["state_directorate"]
    assert "Central Boilers Board" in cert["central_oversight"]
    assert "telemetry_verification_summary" in cert
    assert "sha256_chain_tip_hash" in cert["telemetry_verification_summary"]
    assert "ecdsa_public_key_fingerprint" in cert["telemetry_verification_summary"]
    assert cert["eodb_green_channel_status"] == "APPROVED_REMOTE"
    assert cert["automated_renewal_eligible"] is True
    assert "ecdsa_digital_signature_hex" in cert

    # 3. Inject Overpressure (Scenario 3) -> Certificate must revoke
    client.post("/api/scenario/3")
    cert_revoked_res = client.get("/api/eodb/certificate")
    assert cert_revoked_res.status_code == 200
    cert_revoked = cert_revoked_res.json()
    assert cert_revoked["eodb_green_channel_status"] == "REVOKED_STATUTORY_BREACH"
    assert cert_revoked["automated_renewal_eligible"] is False
    assert len(cert_revoked["revocation_reasons"]) > 0

    # Reset back to normal
    client.post("/api/reset")


