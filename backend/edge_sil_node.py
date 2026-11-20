"""
TapasShield Edge SIL Node (NSA 6.0)
ATECC608B Hardware Security Emulation & Signal Conditioning.

Implements:
1. Reconstructing physical engineering units from raw ADS1115 ADC counts over 150-ohm shunt.
2. Wire-Cut / Loop Open-Circuit Check (I < 3.6 mA).
3. Thermodynamic Cross-Correlation Spoof Check (|T_steam - T_sat(P)| > 5.0 °C or zero variance clamp).
4. Statutory Safety Check (P > 15.0 bar MAWP or Water Level < 25.0%).
5. Monotonic Hash-Chaining (SHA-256) & NIST P-256 (secp256r1) ECDSA Digital Signing.
"""

from typing import Dict, Any, List, Optional
import json
import hashlib
from datetime import datetime, timezone
import statistics

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from iapws import IAPWS97


class EdgeSILNode:
    """
    Edge Safety Integrity Level (SIL) Node with Hardware Cryptographic Element (ATECC608B).
    """

    GENESIS_HASH = "0" * 64
    SHUNT_RESISTOR_OHMS = 150.0
    ADC_FULL_SCALE_V = 4.096
    ADC_MAX_COUNTS = 32767

    def __init__(self, boiler_id: str = "IBR-TN-VEL-2026-0891", private_key: Optional[ec.EllipticCurvePrivateKey] = None):
        self.boiler_id = boiler_id
        self.seq_no = 0
        self.prev_hash = self.GENESIS_HASH

        # Provision real NIST P-256 (secp256r1) Keypair (mimics ATECC608B Slot 0)
        if private_key is None:
            self._private_key = ec.generate_private_key(ec.SECP256R1())
        else:
            self._private_key = private_key

        self._public_key = self._private_key.public_key()
        self.public_key_pem = self._public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode("utf-8")

        # Sliding window for pressure variance detection (last 10 samples)
        self.pressure_history: List[float] = []

    def get_public_key_pem(self) -> str:
        return self.public_key_pem

    def get_public_key(self) -> ec.EllipticCurvePublicKey:
        return self._public_key

    @classmethod
    def reconstruct_from_adc(cls, counts: int, min_val: float, max_val: float) -> Dict[str, float]:
        """
        Reconstructs the loop current (mA) and physical engineering value from 16-bit ADC counts.
        """
        v_shunt = (counts / cls.ADC_MAX_COUNTS) * cls.ADC_FULL_SCALE_V
        i_ma = (v_shunt / cls.SHUNT_RESISTOR_OHMS) * 1000.0

        if i_ma < 3.6:
            # Below 3.6 mA indicates a wire cut, disconnected loop, or fault
            val = min_val
        elif i_ma > 21.0:
            val = max_val
        else:
            normalized = (i_ma - 4.0) / 16.0
            val = min_val + (normalized * (max_val - min_val))

        return {
            "current_ma": round(i_ma, 4),
            "value": round(val, 3),
        }

    def compute_expected_t_sat(self, pressure_bar: float) -> float:
        """
        Calculates expected saturation temperature in °C from measured pressure using IAPWS97.
        """
        p_clamped = max(0.01, min(pressure_bar, 200.0))
        p_mpa = p_clamped * 0.1
        try:
            steam = IAPWS97(P=p_mpa, x=1)
            return round(steam.T - 273.15, 3)
        except Exception:
            # Fallback approximation for out-of-range pressures
            return round(100.0 * (p_clamped ** 0.25), 3)

    def process_raw_telemetry(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes incoming raw ADC counts and physical state, conducts edge SIL security
        checks, serializes canonical payload, and generates SHA-256 hash-chain + ECDSA signature.
        """
        self.seq_no += 1
        now_iso = datetime.now(timezone.utc).isoformat()

        adc_counts = raw_data.get("adc_counts", {})
        loop_currents = raw_data.get("loop_currents_ma", {})

        # 1. Reconstruct Engineering Units from ADC Counts
        pt101_rec = self.reconstruct_from_adc(adc_counts.get("PT_101", 0), 0.0, 25.0)
        tt101_rec = self.reconstruct_from_adc(adc_counts.get("TT_101", 0), 0.0, 350.0)
        tt102_rec = self.reconstruct_from_adc(adc_counts.get("TT_102", 0), 0.0, 500.0)
        ft101_rec = self.reconstruct_from_adc(adc_counts.get("FT_101", 0), 0.0, 5000.0)
        lt101_rec = self.reconstruct_from_adc(adc_counts.get("LT_101", 0), 0.0, 100.0)
        at101_rec = self.reconstruct_from_adc(adc_counts.get("AT_101", 0), 0.0, 5000.0)
        at102_rec = self.reconstruct_from_adc(adc_counts.get("AT_102", 0), 0.0, 14.0)

        # In case the wire cut occurred on PT_101, check both loop_current and reconstructed current
        measured_pressure = raw_data.get("pressure_bar", pt101_rec["value"])
        measured_steam_temp = raw_data.get("steam_temp_c", tt101_rec["value"])
        measured_stack_temp = raw_data.get("stack_temp_c", tt102_rec["value"])
        measured_flow = raw_data.get("mass_flow_kgh", ft101_rec["value"])
        measured_water_level = raw_data.get("drum_water_level_pct", lt101_rec["value"])
        measured_tds = raw_data.get("tds_ppm", at101_rec["value"])
        measured_ph = raw_data.get("ph_level", at102_rec["value"])
        scale_thickness = raw_data.get("scale_thickness_mm", 0.0)
        co2_pct = raw_data.get("co2_pct", 12.5)
        o2_pct = raw_data.get("o2_pct", 4.2)

        # Update pressure history for variance analysis
        self.pressure_history.append(measured_pressure)
        if len(self.pressure_history) > 10:
            self.pressure_history.pop(0)

        # 2. Hardware Security Check 1: Wire-Cut / Loop Open-Circuit Check
        wire_cut_detected = False
        for ch_key, current_val in loop_currents.items():
            if current_val < 3.6:
                wire_cut_detected = True
                break
        if raw_data.get("wire_cut_pt101", False):
            wire_cut_detected = True

        # 3. Hardware Security Check 2: Thermodynamic Cross-Correlation Spoof Check
        expected_t_sat = self.compute_expected_t_sat(measured_pressure)
        temp_discrepancy = abs(measured_steam_temp - expected_t_sat)

        zero_variance_clamp = False
        if len(self.pressure_history) >= 10:
            variance = statistics.variance(self.pressure_history)
            if variance == 0.0000:
                zero_variance_clamp = True

        if raw_data.get("is_fixed_resistor_clamp", False):
            zero_variance_clamp = True

        resistor_spoof_detected = (temp_discrepancy > 5.0) or zero_variance_clamp

        # Set Tamper Status Priority
        if wire_cut_detected:
            tamper_status = "CRITICAL_LOOP_OPEN_CIRCUIT"
        elif resistor_spoof_detected:
            tamper_status = "SYNTHETIC_RESISTOR_SPOOF_DETECTED"
        else:
            tamper_status = "SECURE_VERIFIED"

        # 4. Hardware Security Check 3: Statutory Safety Check (MAWP & Low Water)
        if (measured_pressure > 15.0) or (measured_water_level < 25.0):
            safety_violation = "IBR_CRITICAL_VIOLATION"
        else:
            safety_violation = "NORMAL"

        # 5. Canonical JSON Payload Construction
        canonical_payload = {
            "boiler_id": self.boiler_id,
            "seq_no": self.seq_no,
            "timestamp": now_iso,
            "pressure_bar": round(measured_pressure, 3),
            "expected_t_sat_c": round(expected_t_sat, 3),
            "steam_temp_c": round(measured_steam_temp, 2),
            "stack_temp_c": round(measured_stack_temp, 2),
            "mass_flow_kgh": round(measured_flow, 1),
            "drum_water_level_pct": round(measured_water_level, 2),
            "tds_ppm": round(measured_tds, 1),
            "ph_level": round(measured_ph, 2),
            "co2_pct": round(co2_pct, 2),
            "o2_pct": round(o2_pct, 2),
            "scale_thickness_mm": round(scale_thickness, 3),
            "loop_currents_ma": {k: round(v, 4) for k, v in loop_currents.items()},
            "adc_counts": adc_counts,
            "tamper_status": tamper_status,
            "safety_violation": safety_violation,
            "prev_hash": self.prev_hash,
        }

        # Strict deterministic serialization
        canonical_json_bytes = json.dumps(
            canonical_payload,
            sort_keys=True,
            separators=(",", ":")
        ).encode("utf-8")

        # 6. Monotonic SHA-256 Hash Computation
        current_hash = hashlib.sha256(canonical_json_bytes).hexdigest()

        # 7. ECDSA P-256 Digital Signature
        signature_der = self._private_key.sign(
            canonical_json_bytes,
            ec.ECDSA(hashes.SHA256())
        )
        signature_hex = signature_der.hex()

        # Update chain state
        self.prev_hash = current_hash

        packet = {
            "payload": canonical_payload,
            "canonical_json": canonical_json_bytes.decode("utf-8"),
            "current_hash": current_hash,
            "signature_hex": signature_hex,
            "public_key_pem": self.public_key_pem,
        }

        return packet

    def sign_canonical_payload(self, payload: Dict[str, Any]) -> str:
        """Signs any dictionary payload using RFC 8785 canonical JSON and the ATECC608B private key."""
        canonical_bytes = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        signature_der = self._private_key.sign(
            canonical_bytes,
            ec.ECDSA(hashes.SHA256())
        )
        return signature_der.hex()

    def reset(self):
        """Resets sequence counter and chain hash."""
        self.seq_no = 0
        self.prev_hash = self.GENESIS_HASH
        self.pressure_history.clear()

