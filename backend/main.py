"""
TapasShield Industrial SCADA & Statutory Backend (NSA 6.0)
FastAPI Server + WebSocket Telemetry Stream + Cryptographic Inspector API.
"""

from typing import Dict, Any, List
import asyncio
import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.boiler_twin import BoilerDigitalTwin
from backend.edge_sil_node import EdgeSILNode
from backend.inspector_ledger import InspectorLedger
from backend.predictive_engine import PredictiveEngine

# Global Singletons
twin = BoilerDigitalTwin(boiler_id="IBR-TN-VEL-2026-0891")
edge_node = EdgeSILNode(boiler_id="IBR-TN-VEL-2026-0891")
inspector_ledger = InspectorLedger(public_key=edge_node.get_public_key())
predictive_engine = PredictiveEngine()

# Active WebSocket connections
active_connections: List[WebSocket] = []
simulation_task: asyncio.Task = None
is_running = True

latest_snapshot: Dict[str, Any] = {}


async def broadcast_telemetry(data: Dict[str, Any]):
    """Broadcasts telemetry packet to all connected SCADA and Inspector clients."""
    disconnected = []
    message = json.dumps(data)
    for ws in active_connections:
        try:
            await ws.send_text(message)
        except Exception:
            disconnected.append(ws)
    for ws in disconnected:
        if ws in active_connections:
            active_connections.remove(ws)


def process_simulation_step() -> Dict[str, Any]:
    """Executes a single end-to-end physics -> edge signing -> inspector ledger -> predictive diagnostics step."""
    global latest_snapshot
    raw_state = twin.step()
    packet = edge_node.process_raw_telemetry(raw_state)
    ledger_entry = inspector_ledger.verify_and_append(packet)
    diag = predictive_engine.evaluate_full_diagnostics(
        stack_temp_c=raw_state["stack_temp_c"],
        t_sat_c=raw_state["t_sat_c"],
        ambient_temp_c=raw_state["ambient_temp_c"],
        co2_pct=raw_state["co2_pct"],
        o2_pct=raw_state["o2_pct"],
        boiler_tds_ppm=raw_state["tds_ppm"],
        ph_level=raw_state["ph_level"],
        tick=raw_state["tick"],
    )
    latest_snapshot = {
        "telemetry": packet["payload"],
        "raw_physics": raw_state,
        "cryptography": {
            "current_hash": packet["current_hash"],
            "prev_hash": packet["payload"]["prev_hash"],
            "signature_hex": packet["signature_hex"],
            "public_key_pem": packet["public_key_pem"],
            "signature_valid": ledger_entry["signature_valid"],
            "hash_chain_valid": ledger_entry["hash_chain_valid"],
        },
        "diagnostics": diag,
        "ledger_status": {
            "total_blocks": len(inspector_ledger.blocks),
            "last_seq_no": edge_node.seq_no,
            "statutory_compliant": ledger_entry["statutory_compliant"],
            "tamper_detected": ledger_entry["tamper_detected"],
        },
    }
    return latest_snapshot


async def simulation_loop():
    """Continuous simulation loop running at 1 Hz normal clock."""
    global latest_snapshot, is_running
    while is_running:
        try:
            snapshot = process_simulation_step()
            await broadcast_telemetry(snapshot)
        except Exception as e:
            print(f"[Simulation Loop Error] {e}")

        await asyncio.sleep(1.0)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global simulation_task, is_running
    is_running = True
    # Seed baseline blocks so the ledger and snapshot are populated immediately
    for _ in range(5):
        process_simulation_step()

    simulation_task = asyncio.create_task(simulation_loop())
    yield
    is_running = False
    if simulation_task:
        simulation_task.cancel()


app = FastAPI(
    title="TapasShield IIoT Boiler Platform (NSA 6.0)",
    description="Anti-Falsification Ledger, Hardware SIL Node, and Predictive Maintenance Engine",
    version="6.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/status")
def get_current_status():
    """Returns the most recent system telemetry and diagnostics snapshot."""
    return latest_snapshot


@app.get("/api/public-key")
def get_public_key():
    """Returns the ATECC608B hardware public key in PEM format."""
    return {
        "boiler_id": edge_node.boiler_id,
        "algorithm": "ECDSA_NIST_P256",
        "curve": "secp256r1",
        "public_key_pem": edge_node.get_public_key_pem(),
    }


@app.post("/api/scenario/{scenario_id}")
def trigger_scenario(scenario_id: int):
    """
    Triggers one of the 5 NSA 6.0 test scenarios:
    1: Normal Operation (12 bar)
    2: Simulate Scale Buildup (100x Speed)
    3: Simulate MAWP Over-Pressure & Low-Water Emergency
    4: Simulate Sensor Wire Cut (0 mA)
    5: Simulate Resistor Spoof & DB Log Tamper Attack
    """
    if scenario_id == 1:
        twin.reset_to_normal()
        process_simulation_step()
        return {"scenario": 1, "status": "RESET_NORMAL", "description": "Boiler returned to 12.0 bar steady state with clean tubes."}
    elif scenario_id == 2:
        twin.trigger_scale_buildup()
        process_simulation_step()
        return {"scenario": 2, "status": "SCALE_BUILDUP_ACTIVE", "description": "Waterside scale buildup accelerating (0.1 mm -> 1.8 mm+)."}
    elif scenario_id == 3:
        twin.trigger_overpressure_emergency()
        process_simulation_step()
        return {"scenario": 3, "status": "MAWP_EMERGENCY_ACTIVE", "description": "Pressure spiked to 16.8 bar (>15 bar MAWP), drum water level dropped to 18%."}
    elif scenario_id == 4:
        twin.trigger_wire_cut()
        process_simulation_step()
        return {"scenario": 4, "status": "WIRE_CUT_ACTIVE", "description": "PT-101 4-20mA loop current dropped to 0.00 mA (Wire Cut)."}
    elif scenario_id == 5:
        twin.trigger_resistor_spoof()
        # Also tamper historical DB record
        tamper_result = inspector_ledger.simulate_database_tamper()
        process_simulation_step()
        return {
            "scenario": 5,
            "status": "RESISTOR_SPOOF_AND_DB_TAMPER_ACTIVE",
            "description": "Pressure transmitter clamped to 10.0 bar while steam temp climbed to 212 °C, and historical DB log modified to 11.5 bar without private key.",
            "db_tamper": tamper_result,
        }
    else:
        raise HTTPException(status_code=400, detail="Invalid scenario ID (must be 1-5).")


@app.post("/api/simulate/db-tamper")
def simulate_db_tamper():
    """Directly mutates a historical record in server memory without the hardware private key."""
    result = inspector_ledger.simulate_database_tamper()
    return result


@app.get("/api/ledger")
def get_ledger_records(count: int = 50):
    """Returns recent blocks from the Government Inspector Ledger."""
    return {
        "total_blocks": len(inspector_ledger.blocks),
        "records": inspector_ledger.get_recent_blocks(count=count),
    }


@app.get("/api/ledger/audit")
def audit_ledger():
    """Runs a complete cryptographic and hash-chain audit on all blocks in the ledger."""
    audit_report = inspector_ledger.audit_chain()
    return audit_report


@app.get("/api/eodb/national-registry")
def get_national_registry():
    """
    Returns multi-state national boiler safety and compliance registry across
    Indian industrial clusters (DPIIT & Central Boilers Board oversight).
    """
    return inspector_ledger.get_national_registry(
        live_telemetry=latest_snapshot.get("telemetry"),
        live_diagnostics=latest_snapshot.get("diagnostics"),
        live_crypto=latest_snapshot.get("cryptography"),
    )


@app.get("/api/eodb/certificate")
def get_eodb_certificate():
    """
    Returns cryptographically signed IBR Form-VI Digital Compliance &
    EODB Green-Channel Certificate for automated renewal.
    """
    return inspector_ledger.generate_eodb_certificate(
        edge_node=edge_node,
        latest_snapshot=latest_snapshot,
    )


@app.get("/api/predictive")
def get_predictive_diagnostics():
    """Returns current IS 8753 indirect efficiency, financial losses, and scale RUL."""
    return latest_snapshot.get("diagnostics", {})


@app.post("/api/reset")
def reset_system():
    """Resets digital twin, SIL node, and inspector ledger to pristine state."""
    twin.reset_to_normal()
    edge_node.reset()
    inspector_ledger.clear()
    # Re-seed baseline blocks
    for _ in range(5):
        process_simulation_step()
    return {"status": "SUCCESS", "message": "System reset to initial verified state."}


@app.websocket("/ws/telemetry")
async def websocket_telemetry_endpoint(websocket: WebSocket):
    """Real-time SCADA and Inspector telemetry streaming WebSocket."""
    await websocket.accept()
    active_connections.append(websocket)
    try:
        # Send immediate initial snapshot
        if latest_snapshot:
            await websocket.send_text(json.dumps(latest_snapshot))
        while True:
            # Keep connection alive; accept any incoming control commands
            data = await websocket.receive_text()
            try:
                cmd = json.loads(data)
                if "scenario" in cmd:
                    trigger_scenario(int(cmd["scenario"]))
            except Exception:
                pass
    except WebSocketDisconnect:
        if websocket in active_connections:
            active_connections.remove(websocket)
    except Exception:
        if websocket in active_connections:
            active_connections.remove(websocket)


# Mount Production Frontend Dist if built
import os
from fastapi.staticfiles import StaticFiles

dist_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "dist")
if os.path.exists(dist_path):
    app.mount("/", StaticFiles(directory=dist_path, html=True), name="static")


