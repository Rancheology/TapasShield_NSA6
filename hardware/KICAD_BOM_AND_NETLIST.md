# TapasShield Hardware Architecture: KiCad 8 Schematic, Netlist & BOM Guide

**Document Revision:** 6.0-FINAL  
**Standard Compliance:** Indian Boiler Regulations (IBR 1950 / 2026 Rev), IEC 61508 (SIL-2), CE Industrial EMC EN 61326-1  
**Target Microcontroller:** ESP32-S3-WROOM-1-N16R8 (Xtensa 32-bit Dual-Core @ 240MHz, 16MB Flash, 8MB PSRAM)  
**Hardware Secure Element:** Microchip ATECC608B-TNGISVA-T (ECDSA NIST P-256 Hardware Signer)

---

## 1. System Block Diagram & Power Architecture

```text
[24V DC Industrial Bus]
          │
          ├──> [TPS54302 Buck Converter (24V -> 5.0V @ 3A)]
          │          │
          │          ├──> [AP2112K-3.3 LDO (5.0V -> 3.3V @ 600mA Low Noise)]
          │          │          │
          │          │          ├──> ESP32-S3 Core & Radios
          │          │          ├──> ATECC608B Crypto Element
          │          │          └──> ADS1115 16-Bit Precision ADC
          │          │
          │          └──> Industrial Status LEDs & Optocoupler Biasing
          │
          └──> 4-20mA Current Loops (Loops 1–5: PT-101, TT-101, TT-102, FT-101, AT-101)
                     │
                     └──> [150.0 Ω ±0.05% 25ppm High-Precision Shunt Resistors R1–R5]
                                │
                                └──> RC Low-Pass Filter Network (100 Ω + 100 nF, fc ≈ 16 kHz)
                                           │
                                           ├──> Channels 1–4 (PT-101, TT-101, TT-102, FT-101)
                                           │      └──> U3 ADS1115 (AIN0 - AIN3, I2C 0x48, 16-bit Delta-Sigma)
                                           │
                                           └──> Channel 5 (AT-101 Blowdown Water Quality / TDS & Drum Level)
                                                  └──> U1 ESP32-S3-WROOM-1 Pin 4 (GPIO4 / ADC1_CH3, 12-bit SAR ADC with 11dB/12dB attenuation)
```

---

## 2. Complete Bill of Materials (BOM) for KiCad 8

| RefDes | Quantity | Value / Component | Package / Footprint | Description / Part Number | Manufacturer |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U1** | 1 | ESP32-S3-WROOM-1-N16R8 | SMD Module 41-SMD | Wi-Fi 4 + BLE 5.0, 16MB Flash, 8MB PSRAM | Espressif Systems |
| **U2** | 1 | ATECC608B-TNGISVA-T | SOIC-8 (150 mil) | Secure Hardware Crypto Element (I2C 0x60, ECDSA P-256) | Microchip Tech |
| **U3** | 1 | ADS1115IDGSR | MSOP-10 | 16-Bit 860SPS 4-Channel Delta-Sigma ADC (PGA ±4.096V) | Texas Instruments |
| **U4** | 1 | TPS54302DDCR | SOT-23-6 | 28V 3A Synchronous Step-Down DC-DC Converter | Texas Instruments |
| **U5** | 1 | AP2112K-3.3TRG1 | SOT-23-5 | Ultra-low noise 3.3V 600mA LDO Regulator | Diodes Inc. |
| **D1-D5**| 5 | SMAJ28CA | DO-214AC (SMA) | 28V Bi-Directional TVS Surge Diode for 4-20mA Loops | Littelfuse |
| **D6-D7**| 2 | B540C-13-F | SMC | 40V 5A Schottky Barrier Rectifier (Reverse Polarity) | Diodes Inc. |
| **R1-R5**| 5 | 150.0 Ω ±0.05% 0.25W | 0805 Precision SMD | Precision Current Shunt Resistor (25 ppm/°C, Susumu RR) | Susumu |
| **R6-R10**| 5 | 100 Ω ±1% 0.1W | 0603 SMD | AFE Anti-Aliasing Low-Pass Filter Resistors | Yageo |
| **C1-C5**| 5 | 100 nF 50V X7R | 0603 SMD | AFE Low-Pass Filter Ceramic Capacitors | Murata |
| **R11,R12**| 2 | 4.7 kΩ ±1% | 0603 SMD | I2C Bus Pull-Up Resistors (SDA/SCL) | Panasonic |
| **R13,R14**| 2 | 220 Ω ±1% | 0603 SMD | LED Current Limiting Resistors | Panasonic |
| **LED1** | 1 | Emerald Green (525nm) | 0805 SMD | Verified Telemetry & Valid Cryptographic Signature | Kingbright |
| **LED2** | 1 | Crimson Red (625nm) | 0805 SMD | Tamper / Statutory Overpressure / Wire-Cut Alarm | Kingbright |
| **SW1** | 1 | PTS645SM43SMTR92 | SMD Tactile 6x6mm | SIL Tamper / Wire Break Emulation Pushbutton | C&K Components |
| **J1** | 1 | 2-Pin Screw Terminal 5.08mm | Terminal Block 5.08mm | 24V DC Auxiliary Industrial Power Input | Phoenix Contact |
| **J2-J6**| 5 | 2-Pin Screw Terminal 5.08mm | Terminal Block 5.08mm | Loop 1-5 Inputs (PT-101, TT-101, TT-102, FT-101, AT-101) | Phoenix Contact |
| **L1** | 1 | 10 µH ±20% 3.5A | SMD Inductor 7x7mm | Buck Converter Output Power Inductor (Bourns SRN6045) | Bourns |

---

## 3. Signal Conditioning & Pin-to-Pin Netlist

### 3.1 4-20 mA Precision Analog Front-End (AFE)
Standard 4-20 mA current loops convert physical boiler parameters to loop currents. The current passes through a **150.0 Ω precision shunt resistor** connected to analog ground:
- At **4.0 mA** (Lower Range Value):
  $$V_{\text{shunt}} = 4.0\text{ mA} \times 150.0\,\Omega = 0.600\text{ V}$$
- At **20.0 mA** (Upper Range Value):
  $$V_{\text{shunt}} = 20.0\text{ mA} \times 150.0\,\Omega = 3.000\text{ V}$$
- Under **Over-range / Fault (24.0 mA)**:
  $$V_{\text{shunt}} = 24.0\text{ mA} \times 150.0\,\Omega = 3.600\text{ V}$$

#### 3.1.1 Channels 1–4 (PT-101, TT-101, TT-102, FT-101) via U3 ADS1115:
The ADS1115 operates in single-ended mode with Programmable Gain Amplifier (PGA) set to **$\pm 4.096\text{V}$ (Gain = Two-Thirds)**:
$$1\text{ LSB} = \frac{4.096\text{ V}}{32768} = 125\,\mu\text{V}$$
$$\text{ADC Counts at } 12.0\text{ bar } (11.68\text{ mA}) = \text{int}\left(\frac{1.752\text{ V}}{4.096} \times 32767\right) = 14015\text{ counts}$$

#### 3.1.2 Channel 5 (AT-101 Blowdown TDS & Drum Level) via U1 ESP32-S3 ADC1_CH3:
Loop 5 enters via terminal block `J6`, protected by bi-directional TVS surge diode `D5` (SMAJ28CA), develops voltage across precision shunt `R5` (150.0 Ω ±0.05%), and filters through anti-aliasing RC filter `R10` (100 Ω) + `C5` (100 nF, $f_c \approx 16\text{ kHz}$) directly into `U1 Pin 4 (GPIO4 / ADC1_CH3)`.
The ESP32-S3 internal 12-bit SAR ADC is configured with 11dB attenuation ($0\text{--}3.1\text{V}$ effective linear range, $0\text{--}3.3\text{V}$ full span):
$$1\text{ LSB}_{\text{ESP32}} = \frac{3.300\text{ V}}{4095} \approx 805.8\,\mu\text{V}$$
$$\text{ADC Counts at } 4.0\text{ mA } (0.600\text{ V}) = \text{int}\left(\frac{0.600}{3.300} \times 4095\right) = 744\text{ counts}$$
$$\text{ADC Counts at } 20.0\text{ mA } (3.000\text{ V}) = \text{int}\left(\frac{3.000}{3.300} \times 4095\right) = 3723\text{ counts}$$
$$\text{ADC Counts at Nominal TDS } 2100\text{ ppm } (10.72\text{ mA}, 1.608\text{ V}) = \text{int}\left(\frac{1.608}{3.300} \times 4095\right) = 1996\text{ counts}$$

### 3.2 Microcontroller & Crypto Netlist

| Net Name | Origin Pin | Destination Pin | Description |
| :--- | :--- | :--- | :--- |
| `+3V3_CLEAN` | U5 Pin 5 (VOUT) | U1 Pin 2 (3V3), U2 Pin 8 (VCC), U3 Pin 8 (VDD) | Filtered Low-Noise 3.3V Logic Supply |
| `GND` | U5 Pin 2 (GND) | U1, U2, U3, Shunt Resistors Ground Rail | Common Reference Ground Plane |
| `I2C_SDA` | U1 Pin 13 (GPIO8 / SDA) | U2 Pin 5 (SDA), U3 Pin 9 (SDA), R11 (4.7k Pullup) | Hardware I2C Serial Data Bus |
| `I2C_SCL` | U1 Pin 14 (GPIO9 / SCL) | U2 Pin 6 (SCL), U3 Pin 10 (SCL), R12 (4.7k Pullup) | Hardware I2C Serial Clock Bus |
| `AIN0_PT101`| R6 (100Ω Low-Pass) | U3 Pin 4 (AIN0) | Drum Steam Pressure Loop (0-25 bar) |
| `AIN1_TT101`| R7 (100Ω Low-Pass) | U3 Pin 5 (AIN1) | Steam Header Temp Loop (0-350 °C) |
| `AIN2_TT102`| R8 (100Ω Low-Pass) | U3 Pin 6 (AIN2) | Flue Stack Temp Loop (0-500 °C) |
| `AIN3_FT101`| R9 (100Ω Low-Pass) | U3 Pin 7 (AIN3) | Feedwater & Steam Mass Flow (0-5000 kg/hr) |
| `AIN4_AT101`| R10 (100Ω Low-Pass) / C5 | U1 Pin 4 (GPIO4 / ADC1_CH3) | Blowdown Water TDS & Drum Level Loop (AT-101) |
| `TAMPER_IN` | SW1 Pin 2 | U1 Pin 10 (GPIO5) | Active-Low Tamper Simulation Input |
| `LED_GREEN` | U1 Pin 11 (GPIO6) | R13 (220Ω) -> LED1 Anode | Emerald LED: Verified Cryptographic State |
| `LED_RED` | U1 Pin 12 (GPIO7) | R14 (220Ω) -> LED2 Anode | Crimson LED: Tamper / IBR Alarm State |

---

## 4. Hardware Security & Anti-Tamper Hardening

1. **ATECC608B Hardware Root of Trust:**
   - Provisioned with private key in Slot 0 configured as `WriteConfig = 0x00` (Permanently Locked / Non-Readable).
   - Generates DER-encoded ECDSA P-256 signatures over I2C command `Sign(Mode=0x80, KeyID=0)`.
   - Cannot be dumped, snooped, or cloned via JTAG or fault injection.
2. **Industrial Surge & ESD Protection:**
   - Every 4-20mA channel has a parallel **SMAJ28CA** 28V Bi-directional TVS diode rated for 400W peak surge (IEC 61000-4-5).
   - Series 100 Ω resistor and 100 nF X7R capacitor form an anti-aliasing low-pass filter preventing high-frequency industrial noise from coupling into the ADC.
3. **Power Isolation & Reverse Polarity:**
   - 24V field power is protected by a reverse-bias Schottky diode (`B540C`) and self-resetting PTC polyfuse (1.1A hold).

---

## 5. Physical PCB Dimensions, Stackup & 3D Model Specifications

1. **Board Physical Dimensions:**
   - **Outline:** 120.0 mm × 90.0 mm (`Edge.Cuts` from X=90.0, Y=55.0 to X=210.0, Y=145.0).
   - **Stackup:** 2-Layer FR4, 1.6 mm thickness, 1 oz (35 µm) copper weight.
   - **Mounting Holes:** 4× M3 mechanical mounting holes (`H1–H4`) with 3.2 mm drill and 6.0 mm plated annular rings, inset 5 mm from corners at `(95, 60)`, `(205, 60)`, `(95, 140)`, and `(205, 140)`.
   - **Terminal Block Spacing:** 6× Phoenix MKDS 5.08 mm terminal blocks (`J1–J6`) placed along `X = 102.0 mm` at 11 mm vertical pitch (`Y = 72, 83, 94, 105, 116, 127`), providing >12 mm physical clearance from mounting holes `H1` and `H3` (zero silkscreen, courtyard, or 3D collision).

2. **PCB Routing Rules:**
   - **Top Layer (`F.Cu`):** Strict 45°/90° Manhattan routing with direct pad-to-pad endpoints. Minimum trace width 0.35 mm for analog signals, 0.5–0.6 mm for power rails (`+24V`, `+5V`, `+3V3_CLEAN`).
   - **Bottom Layer (`B.Cu`):** Continuous solid ground copper pour with thermal reliefs (`clearance = 0.35 mm`, `thermal_gap = 0.5 mm`).

3. **Self-Contained 3D VRML 2.0 Library (`hardware/3d_models/`):**
   - 16 custom `#VRML V2.0 utf8` models with realistic PBR material properties:
     * `terminal_2p_508.wrl`: Industrial Phoenix green (`0.0 0.55 0.25`) with silver screw heads and wire-entry cavities.
     * `esp32_s3_wroom.wrl`: Dark green FR4 substrate with brushed metallic silver RF shield can (`0.82 0.84 0.86`) and gold meandering antenna.
     * `soic8.wrl`, `msop10.wrl`, `sot23_6.wrl`, `sot23_5.wrl`: Matte black epoxy IC bodies (`0.12 0.12 0.14`) with silver gull-wing leads.
     * `sma_diode.wrl`, `smc_diode.wrl`: Molded diode packages with silver cathode polarity bands.
     * `inductor_7x7.wrl`: Dark charcoal ferrite shielded cube with silver end electrodes.
     * `smd_0805_r.wrl`, `smd_0603_r.wrl`, `smd_0603_c.wrl`: Realistic passive packages with silver termination caps and black film or ceramic tan bodies.
     * `led_0805_green.wrl`, `led_0805_red.wrl`: Translucent emerald/crimson optical lenses with white carrier bases.
     * `sw_tactile_6x6.wrl`: Metal bracket with black cylindrical tactile actuator button.
     * `m3_mounting_hole.wrl`: Gold/tin plated annular mounting ring.


