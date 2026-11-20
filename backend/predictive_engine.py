"""
TapasShield Predictive Maintenance Engine (NSA 6.0)
Physics-Informed Thermodynamic & Statutory Efficiency Diagnostics per IS 8753.

Calculates:
1. Indirect Boiler Efficiency using Siegert's Dry Flue Gas Loss Formulation.
2. Fuel Financial Penalty in ₹/hour and ₹/year against baseline efficiency.
3. Waterside CaCO3 Scale Thickness Estimation via ΔT_stack (T_stack - T_sat).
4. Remaining Useful Life (RUL) until mandatory statutory acid descaling.
5. Cycles of Concentration (CoC) and Blowdown Water Chemistry balance.
"""

from typing import Dict, Any, List, Optional
import math


class PredictiveEngine:
    """
    Thermodynamic Predictive Maintenance & Financial Loss Engine.
    """

    BASELINE_EFFICIENCY_PCT = 86.50
    BASELINE_FIRING_RATE_KG_H = 350.0
    FUEL_COST_INR_PER_KG = 18.00
    OPERATING_HOURS_PER_YEAR = 8000.0

    CLEAN_DELTA_T_C = 32.0
    SCALE_COEFFICIENT = 38.5  # °C per mm scale
    MANDATORY_DESCALING_DELTA_T_C = 85.0  # Threshold requiring shutdown for cleaning

    FEEDWATER_TDS_PPM = 350.0  # Standard industrial RO/softener feedwater TDS

    def __init__(self):
        self.history_delta_t: List[float] = []
        self.history_ticks: List[int] = []

    def compute_is8753_efficiency(
        self,
        stack_temp_c: float,
        ambient_temp_c: float = 30.0,
        co2_pct: float = 12.5,
        o2_pct: float = 4.2,
    ) -> Dict[str, float]:
        """
        Computes indirect boiler efficiency per Indian Standard IS 8753.
        Dry Flue Gas Loss:
            L_dry% = (0.58 * (T_stack - T_ambient)) / CO2%
        Total Losses:
            L_moisture% ≈ 4.2% (standard hydrogen combustion & humidity loss)
            L_radiation% ≈ 1.5% (surface radiation & convection)
        Efficiency:
            η_boiler% = 100 - (L_dry% + L_moisture% + L_radiation%)
        """
        co2_clamped = max(1.0, min(co2_pct, 20.0))
        delta_t_flue = max(0.0, stack_temp_c - ambient_temp_c)

        # Siegert's dry flue gas loss formula
        loss_dry_flue = (0.58 * delta_t_flue) / co2_clamped
        loss_moisture = 4.20
        loss_radiation = 1.50
        total_losses = loss_dry_flue + loss_moisture + loss_radiation

        efficiency = max(40.0, min(100.0 - total_losses, 95.0))

        return {
            "loss_dry_flue_pct": round(loss_dry_flue, 2),
            "loss_moisture_pct": round(loss_moisture, 2),
            "loss_radiation_pct": round(loss_radiation, 2),
            "total_losses_pct": round(total_losses, 2),
            "efficiency_pct": round(efficiency, 2),
        }

    def compute_financial_loss(self, current_efficiency_pct: float) -> Dict[str, float]:
        """
        Computes financial fuel penalty in ₹/hr and ₹/year resulting from
        heat transfer degradation compared against baseline clean efficiency (86.5%).
        """
        if current_efficiency_pct >= self.BASELINE_EFFICIENCY_PCT:
            return {
                "fuel_penalty_kg_h": 0.0,
                "financial_loss_inr_hr": 0.0,
                "projected_loss_inr_year": 0.0,
            }

        # Energy conservation: Fuel_actual = Fuel_baseline * (eta_baseline / eta_actual)
        fuel_actual_kg_h = self.BASELINE_FIRING_RATE_KG_H * (self.BASELINE_EFFICIENCY_PCT / current_efficiency_pct)
        fuel_penalty_kg_h = max(0.0, fuel_actual_kg_h - self.BASELINE_FIRING_RATE_KG_H)

        loss_inr_hr = fuel_penalty_kg_h * self.FUEL_COST_INR_PER_KG
        projected_loss_year = loss_inr_hr * self.OPERATING_HOURS_PER_YEAR

        return {
            "fuel_penalty_kg_h": round(fuel_penalty_kg_h, 2),
            "financial_loss_inr_hr": round(loss_inr_hr, 2),
            "projected_loss_inr_year": round(projected_loss_year, 2),
        }

    def analyze_scale_and_rul(
        self,
        stack_temp_c: float,
        t_sat_c: float,
        tick: int = 0
    ) -> Dict[str, Any]:
        """
        Calculates CaCO3 scale thickness from stack temperature drift ΔT_stack = T_stack - T_sat.
        Forecasts Remaining Useful Life (RUL) in operating hours and days.
        """
        delta_t = stack_temp_c - t_sat_c
        estimated_scale_mm = max(0.0, (delta_t - self.CLEAN_DELTA_T_C) / self.SCALE_COEFFICIENT)

        self.history_delta_t.append(delta_t)
        self.history_ticks.append(tick)
        if len(self.history_delta_t) > 60:
            self.history_delta_t.pop(0)
            self.history_ticks.pop(0)

        # Compute drift rate (slope) using simple linear regression if enough samples
        drift_rate_c_per_tick = 0.0
        if len(self.history_delta_t) >= 5:
            n = len(self.history_delta_t)
            sum_x = sum(self.history_ticks)
            sum_y = sum(self.history_delta_t)
            sum_xx = sum(x * x for x in self.history_ticks)
            sum_xy = sum(x * y for x, y in zip(self.history_ticks, self.history_delta_t))
            denom = (n * sum_xx - sum_x * sum_x)
            if denom != 0:
                drift_rate_c_per_tick = (n * sum_xy - sum_x * sum_y) / denom

        descaling_required = delta_t >= self.MANDATORY_DESCALING_DELTA_T_C
        remaining_temp_headroom = max(0.0, self.MANDATORY_DESCALING_DELTA_T_C - delta_t)

        # Estimate RUL
        if descaling_required:
            rul_hours = 0.0
            rul_days = 0.0
            rul_status = "CRITICAL_DESCALING_IMMEDIATELY_REQUIRED"
        elif drift_rate_c_per_tick > 0.001:
            # Under active scale accumulation scenario
            ticks_left = remaining_temp_headroom / drift_rate_c_per_tick
            # In accelerated scenario, scale to realistic plant operating equivalent
            rul_hours = round(ticks_left * 2.5, 1)
            rul_days = round(rul_hours / 24.0, 1)
            rul_status = "WARNING_SCALE_ACCUMULATION_DETECTED"
        else:
            # Clean / baseline steady state operation
            # Standard boiler water treatment gives ~180 days between cleanings
            scale_ratio = min(1.0, estimated_scale_mm / 1.38)
            rul_days = round(max(5.0, 180.0 * (1.0 - scale_ratio)), 1)
            rul_hours = round(rul_days * 24.0, 1)
            rul_status = "NOMINAL_CLEAN_TUBES"

        return {
            "delta_t_stack_c": round(delta_t, 2),
            "estimated_scale_mm": round(estimated_scale_mm, 3),
            "descaling_required": descaling_required,
            "remaining_temp_headroom_c": round(remaining_temp_headroom, 2),
            "rul_hours": rul_hours,
            "rul_days": rul_days,
            "rul_status": rul_status,
        }

    def compute_water_chemistry(self, boiler_tds_ppm: float, ph_level: float) -> Dict[str, Any]:
        """
        Computes Cycles of Concentration (CoC) and chemical integrity.
        """
        coc = round(boiler_tds_ppm / max(1.0, self.FEEDWATER_TDS_PPM), 2)
        ph_status = "OPTIMAL"
        if ph_level < 8.5:
            ph_status = "ACIDIC_CORROSION_RISK"
        elif ph_level > 11.5:
            ph_status = "CAUSTIC_EMBRITTLEMENT_RISK"

        tds_status = "OPTIMAL"
        if boiler_tds_ppm > 3500.0:
            tds_status = "BLOWDOWN_REQUIRED_HIGH_CARRYOVER"

        return {
            "cycles_of_concentration": coc,
            "feedwater_tds_ppm": self.FEEDWATER_TDS_PPM,
            "boiler_tds_ppm": boiler_tds_ppm,
            "ph_level": ph_level,
            "ph_status": ph_status,
            "tds_status": tds_status,
        }

    def evaluate_full_diagnostics(
        self,
        stack_temp_c: float,
        t_sat_c: float,
        ambient_temp_c: float,
        co2_pct: float,
        o2_pct: float,
        boiler_tds_ppm: float,
        ph_level: float,
        tick: int = 0
    ) -> Dict[str, Any]:
        """Runs full predictive analytics suite on the current boiler operating state."""
        eff = self.compute_is8753_efficiency(stack_temp_c, ambient_temp_c, co2_pct, o2_pct)
        fin = self.compute_financial_loss(eff["efficiency_pct"])
        scale_rul = self.analyze_scale_and_rul(stack_temp_c, t_sat_c, tick)
        chem = self.compute_water_chemistry(boiler_tds_ppm, ph_level)

        return {
            "efficiency": eff,
            "financial": fin,
            "scale_rul": scale_rul,
            "chemistry": chem,
        }

