# TapasShield SIL-2 Edge Node — Industrial 24V Power & 4–20 mA Loop Wiring Guide

**Hardware Revision:** Rev 6.0-FINAL (`tapasshield_edge.kicad_pcb`, 120×90 mm 2-Layer FR4)  
**Compliance:** Indian Boiler Regulations (IBR 1950 / 2026 Rev), IEC 61508 SIL-2, EN 61326-1  

---

## 1. Industrial 24V DC Power Supply Input (`J1`)

TapasShield is powered directly from the factory control panel's standard **24V DC DIN-rail auxiliary bus** (`10V – 30V DC` wide input tolerance).

| Terminal Block | Pin | Silkscreen Label | Signal Net | Wiring Specification |
| :--- | :--- | :--- | :--- | :--- |
| **J1** (Top-Left Phoenix 5.08mm) | **Pin 1** (Top Square Pad) | `+24V DC IN` | `+24V_IN` | Connect to `+24V DC` DIN-rail supply (`0.75 mm²` / 18 AWG ferrules) |
| **J1** (Top-Left Phoenix 5.08mm) | **Pin 2** (Bottom Round Pad) | `GND / 0V` | `GND` | Connect to Panel `0V / DC Common` & Star Protective Earth (`PE`) |

### Multi-Stage On-Board Power Conditioning
1. **Reverse-Polarity & Surge Stage (`D6`: B540C-13-F):** 40V 5A Schottky barrier rectifier blocks reverse-wiring faults on the factory floor.
2. **Primary Step-Down Buck Converter (`U4`: TPS54302DDCR + `L1`: 10 µH 3.5A + `D7`: B540C):** Steps `24V DC` down to a regulated `+5.0V` rail (`>91%` efficiency, zero thermal heatsink required).
3. **Ultra-Low-Noise Analog/Crypto LDO (`U5`: AP2112K-3.3TRG1):** Filters the `+5.0V` rail into a ripple-free `+3V3_CLEAN` supply powering:
   - **`U1` (ESP32-S3-WROOM-1-N16R8):** Dual-core 240 MHz edge processor + Wi-Fi/BLE telemetry radio.
   - **`U2` (ATECC608B-TNGISVA-T):** Hardware cryptographic root-of-trust (`I2C 0x60`, ECDSA NIST P-256).
   - **`U3` (ADS1115IDGSR):** 16-bit delta-sigma precision ADC (`I2C 0x48`, `±4.096V` PGA reference).

---

## 2. Passive 4–20 mA Current Loop Interception (`J2 – J6`)

All 5 statutory boiler sensor loops connect via industrial 5.08 mm Phoenix screw terminals (`J2` through `J6`). Each channel is protected by a **400W `SMAJ28CA` bi-directional TVS surge diode (`D1–D5`)**, develops `0.600 V – 3.000 V` across a **`150.0 Ω ±0.05%` precision shunt resistor (`R1–R5`)**, and passes through a **`100 Ω + 100 nF` (`fc ≈ 15.9 kHz`) anti-aliasing RC filter (`R6–R10`, `C1–C5`)**:

| Terminal | Statutory Boiler Sensor | Shunt & TVS | ADC Destination | Normal Operating Point |
| :--- | :--- | :--- | :--- | :--- |
| **J2** (`PT-101`) | Drum Steam Pressure (`0–25 bar`) | `R1` (`150Ω`) + `D1` | `U3` ADS1115 `AIN0` (16-bit) | `12.0 bar` → `11.68 mA` (`1.752 V`, `14,015 counts`) |
| **J3** (`TT-101`) | Steam Header Temp (`0–350 °C`) | `R2` (`150Ω`) + `D2` | `U3` ADS1115 `AIN1` (16-bit) | `188.0 °C` → `12.59 mA` (`1.889 V`, `15,112 counts`) |
| **J4** (`TT-102`) | Flue Gas Stack Temp (`0–500 °C`) | `R3` (`150Ω`) + `D3` | `U3` ADS1115 `AIN2` (16-bit) | `220.0 °C` → `11.04 mA` (`1.656 V`, `13,247 counts`) |
| **J5** (`FT-101`) | Steam / Feedwater Flow (`0–5000 kg/hr`) | `R4` (`150Ω`) + `D4` | `U3` ADS1115 `AIN3` (16-bit) | `3500 kg/hr` → `15.20 mA` (`2.280 V`, `18,239 counts`) |
| **J6** (`AT-101`) | Blowdown Water TDS & Drum Level (`0–5000 ppm`) | `R5` (`150Ω`) + `D5` | `U1` ESP32-S3 `Pin 4` (`GPIO4`) | `2100 ppm` → `10.72 mA` (`1.608 V`, `1,996 counts`) |
