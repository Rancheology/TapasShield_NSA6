"""
TapasShield Industrial IIoT Boiler Digital Twin (NSA 6.0)
Thermodynamic Digital Twin & 4-20mA Industrial Current Engine.

Uses real IAPWS-IF97 steam tables to compute exact saturation thermodynamics,
models physical sensor channels, and calculates industrial 4-20mA loop currents
and 16-bit ADS1115 ADC counts over a 150-ohm precision shunt resistor.
"""

from typing import Dict, Any, Optional
import math
import random
from iapws import IAPWS97


class BoilerDigitalTwin:
    """
    Industrial Fire-Tube Steam Boiler Digital Twin.
    Nominal Rating: MAWP = 15.0 bar, Operating Pressure = 12.0 bar (1.2 MPa).
    Steam Generation: 3500 kg/hr saturated steam.
    """

    MAWP_BAR = 15.0
    NORMAL_PRESSURE_BAR = 12.0
    RATED_FLOW_KG_H = 3500.0

    # Channel Definitions: (name, min_val, max_val, unit)
    CHANNELS = {
        "PT_101": {"name": "PT-101 Drum Steam Pressure", "min": 0.0, "max": 25.0, "unit": "bar"},
        "TT_101": {"name": "TT-101 Steam Header Temp", "min": 0.0, "max": 350.0, "unit": "°C"},
        "TT_102": {"name": "TT-102 Flue Stack Temp", "min": 0.0, "max": 500.0, "unit": "°C"},
        "FT_101": {"name": "FT-101 Feedwater/Steam Flow", "min": 0.0, "max": 5000.0, "unit": "kg/hr"},
        "LT_101": {"name": "LT-101 Drum Water Level", "min": 0.0, "max": 100.0, "unit": "%"},
        "AT_101": {"name": "AT-101 Blowdown TDS", "min": 0.0, "max": 5000.0, "unit": "ppm"},
        "AT_102": {"name": "AT-102 Boiler Water pH", "min": 0.0, "max": 14.0, "unit": "pH"},
    }

    SHUNT_RESISTOR_OHMS = 150.0
    ADC_FULL_SCALE_V = 4.096
    ADC_MAX_COUNTS = 32767  # 16-bit signed positive range for ADS1115

    def __init__(self, boiler_id: str = "IBR-TN-VEL-2026-0891"):
        self.boiler_id = boiler_id
        self.pressure_bar = self.NORMAL_PRESSURE_BAR
        self.scale_thickness_mm = 0.0
        self.drum_water_level_pct = 65.0
        self.mass_flow_kgh = self.RATED_FLOW_KG_H
        self.co2_pct = 12.5
        self.o2_pct = 4.2
        self.tds_ppm = 2100.0
        self.ph_level = 9.8
        self.ambient_temp_c = 30.0

        # Fault Injection Flags
        self.wire_cut_pt101 = False
        self.resistor_spoof_active = False
        self.spoofed_pressure_bar = 10.0
        self.spoofed_steam_temp_c = 212.0
        self.scale_buildup_active = False
        self.scale_ramp_rate = 0.02  # mm per tick in 100x speed
        self.overpressure_active = False

        self.tick_count = 0

    @staticmethod
    def calculate_saturation_properties(pressure_bar: float) -> Dict[str, float]:
        """
        Calculates exact saturated steam properties using IAPWS-IF97 formulation.
        Pressure input in bar, converted to MPa for IAPWS97.
        """
        # IAPWS97 accepts pressure in MPa
        p_clamped = max(0.01, min(pressure_bar, 200.0))
        p_mpa = p_clamped * 0.1

        try:
            steam = IAPWS97(P=p_mpa, x=1)
            water = IAPWS97(P=p_mpa, x=0)
            t_sat_c = steam.T - 273.15
            h_g = steam.h  # kJ/kg
            h_f = water.h  # kJ/kg
            h_fg = h_g - h_f
            v_g = steam.v  # m^3/kg
            rho_g = steam.rho  # kg/m^3
        except Exception:
            # Fallback to Antoine approximation if outside standard steam boundary
            t_sat_c = 100.0 * (p_clamped ** 0.25)
            h_fg = 2257.0 - (t_sat_c - 100.0) * 2.3
            v_g = 0.15
            rho_g = 6.67

        return {
            "p_mpa": p_mpa,
            "t_sat_c": round(t_sat_c, 3),
            "h_fg_kj_kg": round(h_fg, 2),
            "v_g_m3_kg": round(v_g, 4),
            "rho_g_kg_m3": round(rho_g, 3),
        }

    @classmethod
    def value_to_4_20ma(cls, value: float, min_val: float, max_val: float) -> float:
        """
        Converts a physical engineering unit to standard industrial 4-20 mA loop current.
        I_mA = 4.0 + ((X - X_min) / (X_max - X_min)) * 16.0
        """
        if max_val == min_val:
            return 4.0
        clamped_val = max(min_val, min(value, max_val))
        normalized = (clamped_val - min_val) / (max_val - min_val)
        return round(4.0 + (normalized * 16.0), 4)

    @classmethod
    def current_to_adc_counts(cls, i_ma: float) -> int:
        """
        Converts loop current (mA) across 150 Ohm shunt to 16-bit ADS1115 ADC counts.
        V_shunt = I_mA * 0.150 V (since mA * 150 Ohm = mV = * 0.150 V)
        ADC_Counts = int((V_shunt / 4.096) * 32767)
        """
        if i_ma <= 0.0:
            return 0
        v_shunt = (i_ma / 1000.0) * cls.SHUNT_RESISTOR_OHMS
        counts = int((v_shunt / cls.ADC_FULL_SCALE_V) * cls.ADC_MAX_COUNTS)
        return max(0, min(counts, cls.ADC_MAX_COUNTS))

    @classmethod
    def adc_counts_to_value(cls, counts: int, min_val: float, max_val: float) -> float:
        """
        Reconstructs physical engineering value from 16-bit ADS1115 ADC counts.
        """
        v_shunt = (counts / cls.ADC_MAX_COUNTS) * cls.ADC_FULL_SCALE_V
        i_ma = (v_shunt / cls.SHUNT_RESISTOR_OHMS) * 1000.0
        if i_ma < 4.0:
            return min_val
        normalized = (i_ma - 4.0) / 16.0
        val = min_val + (normalized * (max_val - min_val))
        return round(max(min_val, min(val, max_val)), 3)

    def step(self) -> Dict[str, Any]:
        """
        Advances the simulation clock by 1 tick and produces the physical telemetry state.
        """
        self.tick_count += 1

        # 1. Update Scenario States
        if self.scale_buildup_active:
            self.scale_thickness_mm = min(2.5, self.scale_thickness_mm + self.scale_ramp_rate)

        if self.overpressure_active:
            # Overpressure spike to 16.8 bar and water level drops to 18%
            self.pressure_bar = 16.80
            self.drum_water_level_pct = 18.00
        elif not self.resistor_spoof_active:
            # Subtle natural industrial drift around 12.0 bar (+/- 0.08 bar)
            noise = (math.sin(self.tick_count * 0.25) * 0.05) + ((random.random() - 0.5) * 0.03)
            self.pressure_bar = round(self.NORMAL_PRESSURE_BAR + noise, 3)

        # 2. Thermodynamic Calculations via IAPWS97
        sat_props = self.calculate_saturation_properties(self.pressure_bar)
        t_sat = sat_props["t_sat_c"]

        # Steam header temp TT-101 tracks T_sat with slight superheat/noise (+0.5 to +1.5 C)
        steam_temp_c = round(t_sat + 0.8 + (math.cos(self.tick_count * 0.18) * 0.2), 2)

        # Stack Temp TT-102 per specification:
        # T_stack = T_sat + 32.0 + 38.5 * d_scale
        base_stack_delta = 32.0 + (38.5 * self.scale_thickness_mm)
        stack_temp_c = round(t_sat + base_stack_delta + ((random.random() - 0.5) * 0.2), 2)

        # 3. Apply Resistor Spoof if active
        # Sensor clamped to fake 10.0 bar while actual steam temp climbs to 212 C
        reported_pressure = self.pressure_bar
        reported_steam_temp = steam_temp_c
        is_fixed_resistor_clamp = False

        if self.resistor_spoof_active:
            reported_pressure = self.spoofed_pressure_bar
            reported_steam_temp = self.spoofed_steam_temp_c
            is_fixed_resistor_clamp = True

        # 4. Generate Industrial 4-20 mA Currents
        pt101_ma = self.value_to_4_20ma(reported_pressure, 0.0, 25.0)
        if self.wire_cut_pt101:
            pt101_ma = 0.00  # Wire cut / loop break

        tt101_ma = self.value_to_4_20ma(reported_steam_temp, 0.0, 350.0)
        tt102_ma = self.value_to_4_20ma(stack_temp_c, 0.0, 500.0)
        ft101_ma = self.value_to_4_20ma(self.mass_flow_kgh, 0.0, 5000.0)
        lt101_ma = self.value_to_4_20ma(self.drum_water_level_pct, 0.0, 100.0)
        at101_ma = self.value_to_4_20ma(self.tds_ppm, 0.0, 5000.0)
        at102_ma = self.value_to_4_20ma(self.ph_level, 0.0, 14.0)

        # 5. Quantize to 16-bit ADS1115 ADC counts
        adc_counts = {
            "PT_101": self.current_to_adc_counts(pt101_ma),
            "TT_101": self.current_to_adc_counts(tt101_ma),
            "TT_102": self.current_to_adc_counts(tt102_ma),
            "FT_101": self.current_to_adc_counts(ft101_ma),
            "LT_101": self.current_to_adc_counts(lt101_ma),
            "AT_101": self.current_to_adc_counts(at101_ma),
            "AT_102": self.current_to_adc_counts(at102_ma),
        }

        loop_currents = {
            "PT_101": pt101_ma,
            "TT_101": tt101_ma,
            "TT_102": tt102_ma,
            "FT_101": ft101_ma,
            "LT_101": lt101_ma,
            "AT_101": at101_ma,
            "AT_102": at102_ma,
        }

        return {
            "boiler_id": self.boiler_id,
            "tick": self.tick_count,
            "pressure_bar": reported_pressure,
            "true_physics_pressure_bar": self.pressure_bar,
            "t_sat_c": t_sat,
            "h_fg_kj_kg": sat_props["h_fg_kj_kg"],
            "steam_temp_c": reported_steam_temp,
            "stack_temp_c": stack_temp_c,
            "mass_flow_kgh": self.mass_flow_kgh,
            "drum_water_level_pct": self.drum_water_level_pct,
            "tds_ppm": self.tds_ppm,
            "ph_level": self.ph_level,
            "co2_pct": self.co2_pct,
            "o2_pct": self.o2_pct,
            "ambient_temp_c": self.ambient_temp_c,
            "scale_thickness_mm": round(self.scale_thickness_mm, 3),
            "loop_currents_ma": loop_currents,
            "adc_counts": adc_counts,
            "is_fixed_resistor_clamp": is_fixed_resistor_clamp,
            "wire_cut_pt101": self.wire_cut_pt101,
        }

    def reset_to_normal(self):
        """Resets all simulation parameters and fault states to normal operating point."""
        self.pressure_bar = self.NORMAL_PRESSURE_BAR
        self.scale_thickness_mm = 0.0
        self.drum_water_level_pct = 65.0
        self.mass_flow_kgh = self.RATED_FLOW_KG_H
        self.co2_pct = 12.5
        self.o2_pct = 4.2
        self.tds_ppm = 2100.0
        self.ph_level = 9.8
        self.wire_cut_pt101 = False
        self.resistor_spoof_active = False
        self.scale_buildup_active = False
        self.overpressure_active = False

    def trigger_scale_buildup(self):
        """Accelerates scale buildup from 1.15 mm to 1.8 mm+ for rapid 100x live demonstration."""
        self.scale_thickness_mm = 1.15
        self.scale_ramp_rate = 0.12
        self.scale_buildup_active = True
        self.wire_cut_pt101 = False
        self.resistor_spoof_active = False
        self.overpressure_active = False

    def trigger_overpressure_emergency(self):
        """Spikes pressure to 16.8 bar and drops water level to 18%."""
        self.overpressure_active = True
        self.wire_cut_pt101 = False
        self.resistor_spoof_active = False
        self.scale_buildup_active = False

    def trigger_wire_cut(self):
        """Simulates physical wire cut on PT-101 loop transmitter (0.00 mA)."""
        self.wire_cut_pt101 = True
        self.resistor_spoof_active = False
        self.overpressure_active = False

    def trigger_resistor_spoof(self):
        """Clamps pressure reading to fake 10.0 bar while actual steam temp climbs to 212 C."""
        self.resistor_spoof_active = True
        self.spoofed_pressure_bar = 10.00
        self.spoofed_steam_temp_c = 212.00
        self.wire_cut_pt101 = False
        self.overpressure_active = False

