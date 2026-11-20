"""
TapasShield System Verification Test Suite (NSA 6.0)
Mandatory Physics, 4-20mA Signal Conditioning, Edge Spoof Detection,
and Elliptic-Curve Cryptographic Integrity Verification.

All 6 test cases must pass 100% green:
1. test_iapws_saturation_physics
2. test_4_20ma_conversion_and_adc_quantization
3. test_wire_cut_loop_open_circuit
4. test_thermodynamic_cross_correlation_spoof_detection
5. test_ecdsa_sha256_hashchain_verification
6. test_cryptographic_tamper_rejection
"""

import pytest
import math
from iapws import IAPWS97

from backend.boiler_twin import BoilerDigitalTwin
from backend.edge_sil_node import EdgeSILNode
from backend.inspector_ledger import InspectorLedger
from backend.predictive_engine import PredictiveEngine


def test_iapws_saturation_physics():
    """
    Test 1: Real IAPWS-IF97 thermodynamics.
    Verifies that at 12.0 bar (1.2 MPa), T_sat is ~187.96 °C and h_fg is accurate.
    Verifies stack temperature calculation under clean and scaled tube conditions.
    """
    p_bar = 12.0
    sat = BoilerDigitalTwin.calculate_saturation_properties(p_bar)

    assert abs(sat["t_sat_c"] - 187.96) < 0.15, f"Expected T_sat ~187.96 C, got {sat['t_sat_c']}"
    assert sat["h_fg_kj_kg"] > 1900.0, f"Expected latent heat h_fg > 1900 kJ/kg, got {sat['h_fg_kj_kg']}"

    # Verify clean tube stack temp: T_stack = T_sat + 32.0 C
    twin = BoilerDigitalTwin()
    twin.reset_to_normal()
    state = twin.step()
    t_sat = state["t_sat_c"]
    assert abs(state["stack_temp_c"] - (t_sat + 32.0)) < 1.0

    # Verify scaled tube stack temp: T_stack = T_sat + 32.0 + 38.5 * d_scale
    twin.scale_thickness_mm = 1.0
    state_scaled = twin.step()
    expected_stack = t_sat + 32.0 + 38.5 * 1.0
    assert abs(state_scaled["stack_temp_c"] - expected_stack) < 1.5


def test_4_20ma_conversion_and_adc_quantization():
    """
    Test 2: Industrial 4-20 mA loop current and ADS1115 16-bit ADC count quantization.
    Channel 1 PT-101: 0-25 bar. At 12.0 bar:
    I_mA = 4.0 + (12.0 / 25.0) * 16.0 = 11.68 mA
    V_shunt = 11.68 mA * 150 Ohm = 1.752 V
    ADC_Counts = int((1.752 / 4.096) * 32767) = 14015
    """
    p_val = 12.0
    min_p = 0.0
    max_p = 25.0

    current_ma = BoilerDigitalTwin.value_to_4_20ma(p_val, min_p, max_p)
    assert abs(current_ma - 11.68) < 0.01, f"Expected 11.68 mA, got {current_ma}"

    adc_counts = BoilerDigitalTwin.current_to_adc_counts(current_ma)
    # Expected: int((11.68 * 0.150 / 4.096) * 32767) = 14015
    assert abs(adc_counts - 14015) <= 2, f"Expected ~14015 counts, got {adc_counts}"

    # Verify Edge AFE reconstruction
    rec = EdgeSILNode.reconstruct_from_adc(adc_counts, min_p, max_p)
    assert abs(rec["value"] - p_val) < 0.05, f"Reconstructed {rec['value']} bar != {p_val} bar"
    assert abs(rec["current_ma"] - current_ma) < 0.05

    # Boundary tests
    assert BoilerDigitalTwin.value_to_4_20ma(0.0, 0.0, 25.0) == 4.0
    assert BoilerDigitalTwin.value_to_4_20ma(25.0, 0.0, 25.0) == 20.0
    assert BoilerDigitalTwin.current_to_adc_counts(0.0) == 0


def test_wire_cut_loop_open_circuit():
    """
    Test 3: Wire-cut / open-circuit detection.
    When a transmitter cable is severed, loop current drops below 3.6 mA (0.0 mA).
    The Edge SIL Node must detect this and flag CRITICAL_LOOP_OPEN_CIRCUIT.
    """
    twin = BoilerDigitalTwin()
    edge = EdgeSILNode()
    ledger = InspectorLedger(public_key=edge.get_public_key())

    twin.trigger_wire_cut()
    state = twin.step()

    assert state["loop_currents_ma"]["PT_101"] == 0.00
    assert state["adc_counts"]["PT_101"] == 0

    packet = edge.process_raw_telemetry(state)
    assert packet["payload"]["tamper_status"] == "CRITICAL_LOOP_OPEN_CIRCUIT"

    ledger_entry = ledger.verify_and_append(packet)
    assert ledger_entry["tamper_detected"] is True
    assert ledger_entry["statutory_compliant"] is False


def test_thermodynamic_cross_correlation_spoof_detection():
    """
    Test 4: Cross-correlation spoof detector.
    If an adversary clamps the pressure sensor to a fixed 10.0 bar (where T_sat ~ 179.9 °C)
    while the steam temperature climbs to 212.0 °C:
    Discrepancy |212.0 - 179.9| = 32.1 °C > 5.0 °C threshold.
    The Edge SIL Node must flag SYNTHETIC_RESISTOR_SPOOF_DETECTED.
    """
    twin = BoilerDigitalTwin()
    edge = EdgeSILNode()

    twin.trigger_resistor_spoof()
    state = twin.step()

    packet = edge.process_raw_telemetry(state)
    assert packet["payload"]["tamper_status"] == "SYNTHETIC_RESISTOR_SPOOF_DETECTED"

    # Also test zero-variance clamp detection
    edge2 = EdgeSILNode()
    # Feed 10 samples with identical pressure
    for _ in range(10):
        normal_state = {
            "pressure_bar": 12.000,
            "steam_temp_c": 188.0,
            "stack_temp_c": 220.0,
            "mass_flow_kgh": 3500.0,
            "drum_water_level_pct": 65.0,
            "tds_ppm": 2100.0,
            "ph_level": 9.8,
            "scale_thickness_mm": 0.0,
            "co2_pct": 12.5,
            "o2_pct": 4.2,
            "adc_counts": {"PT_101": 14015},
            "loop_currents_ma": {"PT_101": 11.68},
            "is_fixed_resistor_clamp": True,
        }
        pkt = edge2.process_raw_telemetry(normal_state)
    assert pkt["payload"]["tamper_status"] == "SYNTHETIC_RESISTOR_SPOOF_DETECTED"


def test_ecdsa_sha256_hashchain_verification():
    """
    Test 5: Real NIST P-256 ECDSA digital signatures and SHA-256 hash chaining.
    Every packet must have valid monotonic seq_no, correct previous hash link,
    and a cryptographically valid ECDSA signature verifiable by the Inspector Ledger.
    """
    twin = BoilerDigitalTwin()
    edge = EdgeSILNode()
    ledger = InspectorLedger(public_key=edge.get_public_key())

    twin.reset_to_normal()
    prev_hash = "0" * 64

    for expected_seq in range(1, 6):
        raw_state = twin.step()
        packet = edge.process_raw_telemetry(raw_state)

        # Verify monotonic sequence and hash linkage
        assert packet["payload"]["seq_no"] == expected_seq
        assert packet["payload"]["prev_hash"] == prev_hash

        # Inspector Ledger Ingestion & Verification
        entry = ledger.verify_and_append(packet)
        assert entry["signature_valid"] is True, f"ECDSA Signature failed on seq #{expected_seq}"
        assert entry["hash_chain_valid"] is True, f"Hash chaining failed on seq #{expected_seq}"
        assert entry["tamper_detected"] is False

        prev_hash = packet["current_hash"]

    # Full ledger audit should pass
    audit = ledger.audit_chain()
    assert audit["chain_valid"] is True
    assert audit["total_blocks"] == 5
    assert audit["tampered_block_seq"] is None


def test_cryptographic_tamper_rejection():
    """
    Test 6: Anti-Falsification Ledger audit scan.
    If an attacker or rogue administrator modifies historical records in the database
    (e.g. changing 16.8 bar emergency overpressure down to 11.5 bar 'safe'),
    the audit scan MUST detect the fraud, reject the broken signature,
    and pinpoint the exact sequence number where the chain broke.
    """
    twin = BoilerDigitalTwin()
    edge = EdgeSILNode()
    ledger = InspectorLedger(public_key=edge.get_public_key())

    twin.reset_to_normal()
    # Ingest 3 normal blocks
    for _ in range(3):
        raw = twin.step()
        pkt = edge.process_raw_telemetry(raw)
        ledger.verify_and_append(pkt)

    # Ingest 1 overpressure block (seq 4)
    twin.trigger_overpressure_emergency()
    raw = twin.step()
    pkt = edge.process_raw_telemetry(raw)
    ledger.verify_and_append(pkt)
    tampered_target_seq = pkt["payload"]["seq_no"]

    # Ingest 2 more blocks
    for _ in range(2):
        raw = twin.step()
        pkt = edge.process_raw_telemetry(raw)
        ledger.verify_and_append(pkt)

    # Verify audit is valid before database attack
    initial_audit = ledger.audit_chain()
    assert initial_audit["chain_valid"] is True

    # Execute unauthorized database modification (attacker alters seq 4 from 16.8 bar to 11.5 bar)
    tamper_result = ledger.simulate_database_tamper(target_seq=tampered_target_seq)
    assert tamper_result["success"] is True

    # Forensic audit scan
    audit = ledger.audit_chain()
    assert audit["chain_valid"] is False, "Forensic audit failed to catch database modification!"
    assert audit["tampered_block_seq"] == tampered_target_seq, (
        f"Expected audit to catch block #{tampered_target_seq}, got {audit['tampered_block_seq']}"
    )
    assert "TAMPER DETECTED" in audit["message"] or "SIGNATURE INVALID" in audit["message"]

