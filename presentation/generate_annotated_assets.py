#!/usr/bin/env python3
"""
TapasShield Annotated Assets & Deployment Diagrams Generator
Generates:
1. presentation/diagram_industrial_deployment.png:
   Visual architecture of physical boiler room, transmitters, 35mm DIN-rail TapasShield node,
   Phoenix screw terminal non-intrusive pass-through, and dual cloud stream.
2. presentation/diagram_pcb_3d_annotated.png:
   Publication-grade annotated 3D KiCad PCB render with explicit callouts for all subsystems.
3. Crops of live website UI elements (P&ID schematic, Loop Current Monitor, National Grid, Crypto Blocks).
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont

DARK_BG = "#090D16"
PANEL_BG = "#0F172A"
CARD_BG = "#131D31"
TEXT_COLOR = "#F8FAFC"
MUTED_TEXT = "#94A3B8"
EMERALD = "#10B981"
CYAN = "#38BDF8"
AMBER = "#F59E0B"
CRIMSON = "#EF4444"
INDIGO = "#818CF8"

def generate_crops():
    print("[1/3] Generating clean UI crops from live website captures...")
    src_full = "presentation/screenshots/screenshot_pid_schematic.png"
    if os.path.exists(src_full):
        img = Image.open(src_full)
        w, h = img.size

        # 1. P&ID Twin Crop (top portion)
        box_pid = (int(0.02 * w), int(0.09 * h), int(0.98 * w), int(0.40 * h))
        img.crop(box_pid).save("presentation/screenshots/crop_pid_schematic_twin.png")
        print("  -> Saved: crop_pid_schematic_twin.png")

        # 2. National Multi-State Cluster Grid (mid-right portion)
        box_grid = (int(0.51 * w), int(0.48 * h), int(0.98 * w), int(0.74 * h))
        img.crop(box_grid).save("presentation/screenshots/crop_national_cluster_grid.png")
        print("  -> Saved: crop_national_cluster_grid.png")

        # 3. Cryptographic Hash Chain Ledger (bottom-right portion)
        box_chain = (int(0.51 * w), int(0.74 * h), int(0.98 * w), int(0.96 * h))
        img.crop(box_chain).save("presentation/screenshots/crop_crypto_hash_chain.png")
        print("  -> Saved: crop_crypto_hash_chain.png")

        # 4. Loop Current Monitor (bottom-left portion with margin for title)
        box_loop = (int(0.02 * w), int(0.725 * h), int(0.49 * w), int(0.96 * h))
        img.crop(box_loop).save("presentation/screenshots/crop_loop_current_monitor.png")
        print("  -> Saved: crop_loop_current_monitor.png")

    # 5. Tight crop of Form-VI Certificate Modal
    cert_full = "presentation/screenshots/screenshot_form_vi_certificate.png"
    if os.path.exists(cert_full):
        cimg = Image.open(cert_full)
        cw, ch = cimg.size
        # The modal sits in the center: ~25% to 75% width, ~10% to 90% height
        box_cert = (int(0.28 * cw), int(0.12 * ch), int(0.72 * cw), int(0.88 * ch))
        cimg.crop(box_cert).save("presentation/screenshots/crop_form_vi_modal.png")
        print("  -> Saved: crop_form_vi_modal.png")

    # 6. Tight crop of Forensic Tamper Alert
    tamper_full = "presentation/screenshots/screenshot_forensic_audit_tamper.png"
    if os.path.exists(tamper_full):
        timg = Image.open(tamper_full)
        tw, th = timg.size
        # The tamper banner is in the lower 35% of the screen
        box_tamper = (int(0.02 * tw), int(0.70 * th), int(0.98 * tw), int(0.96 * th))
        timg.crop(box_tamper).save("presentation/screenshots/crop_forensic_tamper_alert.png")
        print("  -> Saved: crop_forensic_tamper_alert.png")

    # 7. Clean KiCad 3D Viewer Crop
    cad_full = "presentation/screenshots/screenshot_hardware_cad.png"
    if os.path.exists(cad_full):
        kimg = Image.open(cad_full)
        kw, kh = kimg.size
        # The hardware CAD viewer starts around 50% height down to 98%
        box_cad = (int(0.02 * kw), int(0.50 * kh), int(0.98 * kw), int(0.96 * kh))
        kimg.crop(box_cad).save("presentation/screenshots/crop_kicad_cad_viewer.png")
        print("  -> Saved: crop_kicad_cad_viewer.png")

def generate_diagram_industrial_deployment():
    print("[2/3] Generating Industrial Boiler Physical Deployment Diagram...")
    fig, ax = plt.subplots(figsize=(14, 7.8), dpi=300)
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 7.8)
    ax.axis("off")

    # Header Title
    ax.text(0.5, 7.35, "TAPASSHIELD INDUSTRIAL DEPLOYMENT & RETROFIT TOPOLOGY", color=CYAN, fontsize=17, fontweight="bold")
    ax.text(0.5, 6.95, "Non-Intrusive 4–20 mA Interception inside Boiler Room Control Panel (Zero Pressure Vessel Alterations)", color=MUTED_TEXT, fontsize=11.5)

    # -------------------------------------------------------------
    # ZONE 1: THE INDUSTRIAL BOILER ROOM (LEFT)
    # -------------------------------------------------------------
    zone1_box = patches.FancyBboxPatch((0.4, 0.5), 4.2, 6.1, boxstyle="round,pad=0.15", facecolor=CARD_BG, edgecolor="#334155", linewidth=1.5)
    ax.add_patch(zone1_box)
    ax.text(0.6, 6.25, "ZONE 1: BOILER ROOM SENSORS", color=EMERALD, fontsize=13.0, fontweight="bold")
    ax.text(0.6, 5.95, "Fire-Tube / Water-Tube (MAWP 15.0 bar)", color=MUTED_TEXT, fontsize=10.0)

    # Boiler Drum graphic
    drum = patches.FancyBboxPatch((0.7, 4.3), 3.6, 1.45, boxstyle="round,pad=0.15", facecolor="#1E293B", edgecolor=CYAN, linewidth=1.8)
    ax.add_patch(drum)
    ax.text(2.5, 5.25, "STEAM BOILER DRUM", color=TEXT_COLOR, fontsize=12.5, fontweight="bold", ha="center")
    ax.text(2.5, 4.90, "188°C Saturated Steam @ 12.0 bar", color=MUTED_TEXT, fontsize=9.5, ha="center")

    # Water Level inside drum
    water = patches.Rectangle((0.75, 4.35), 3.5, 0.45, facecolor="#0284C7", alpha=0.35)
    ax.add_patch(water)
    ax.text(2.5, 4.55, "Water Level: 65% (TDS 2100 ppm)", color="#38BDF8", fontsize=9.5, ha="center")

    # Burner / Furnace
    burner = patches.FancyBboxPatch((0.7, 2.85), 1.7, 1.25, boxstyle="round,pad=0.1", facecolor="#1E293B", edgecolor=AMBER, linewidth=1.5)
    ax.add_patch(burner)
    ax.text(1.55, 3.65, "BURNER UNIT", color=AMBER, fontsize=11.0, fontweight="bold", ha="center")
    ax.text(1.55, 3.20, "Heavy Oil / Gas\nFiring: 100%", color=MUTED_TEXT, fontsize=9.2, ha="center")

    # Flue Stack
    stack = patches.Rectangle((2.6, 2.85), 1.7, 1.25, facecolor="#1E293B", edgecolor=CRIMSON, linewidth=1.5)
    ax.add_patch(stack)
    ax.text(3.45, 3.65, "FLUE STACK", color=CRIMSON, fontsize=11.0, fontweight="bold", ha="center")
    ax.text(3.45, 3.20, "Stack: 220°C\nIS 8753 Flue Gas", color=MUTED_TEXT, fontsize=9.2, ha="center")

    # 5 Sensor Callout Badges on the boiler (arranged vertically in lower half)
    sensors = [
        {"tag": "PT-101", "name": "Drum Pressure (0-25 bar)", "y": 2.40, "color": CYAN},
        {"tag": "TT-101", "name": "Steam Header Temp (0-350°C)", "y": 1.95, "color": EMERALD},
        {"tag": "TT-102", "name": "Flue Gas Temp (0-500°C)", "y": 1.50, "color": CRIMSON},
        {"tag": "FT-101", "name": "Steam Flow (0-5000 kg/hr)", "y": 1.05, "color": AMBER},
        {"tag": "AT-101", "name": "Blowdown TDS (0-5000 ppm)", "y": 0.60, "color": INDIGO},
    ]

    for s in sensors:
        s_box = patches.FancyBboxPatch((0.6, s["y"] - 0.16), 3.8, 0.36, boxstyle="round,pad=0.05", facecolor="#0B132B", edgecolor=s["color"], linewidth=1.2)
        ax.add_patch(s_box)
        ax.text(0.75, s["y"], f"[{s['tag']}] {s['name']}", color=s["color"], fontsize=9.2, fontweight="bold", va="center")
        ax.text(4.25, s["y"], "4–20 mA", color=TEXT_COLOR, fontsize=8.8, fontweight="bold", va="center", ha="right")

    # -------------------------------------------------------------
    # ZONE 2: BOILER ROOM CONTROL PANEL / BMS (CENTER)
    # -------------------------------------------------------------
    zone2_box = patches.FancyBboxPatch((5.0, 0.5), 4.6, 6.1, boxstyle="round,pad=0.15", facecolor=CARD_BG, edgecolor=EMERALD, linewidth=2.0)
    ax.add_patch(zone2_box)
    ax.text(5.2, 6.25, "ZONE 2: ELECTRICAL BMS CABINET", color=EMERALD, fontsize=12.5, fontweight="bold")
    ax.text(5.2, 5.95, "Standard 35mm Industrial DIN-Rail | IP66 Die-Cast Enclosure", color=MUTED_TEXT, fontsize=9.5)

    # DIN Rail Bar Graphic at the top
    din_rail = patches.Rectangle((5.2, 5.55), 4.2, 0.28, facecolor="#475569", edgecolor="#94A3B8", linewidth=1.0)
    ax.add_patch(din_rail)
    ax.text(7.3, 5.69, "35mm TOP-HAT DIN RAIL (EN 50022)", color="#F8FAFC", fontsize=8.8, fontweight="bold", ha="center", va="center")

    # TapasShield Hardware Node Enclosure Box
    ts_node = patches.FancyBboxPatch((5.25, 1.35), 4.1, 4.05, boxstyle="round,pad=0.15", facecolor="#090D16", edgecolor=EMERALD, linewidth=2.0)
    ax.add_patch(ts_node)

    # Enclosure Header
    ax.text(7.3, 5.15, "TAPASSHIELD SIL-2 EDGE NODE", color=TEXT_COLOR, fontsize=12.0, fontweight="bold", ha="center")
    ax.text(7.3, 4.88, "120 × 90 mm 2-Layer FR4 | ESP32-S3 + ATECC608B", color=CYAN, fontsize=9.2, ha="center")

    # Terminal block representations
    term_labels = [
        ("J1: 24V DC Auxiliary Power", "#F59E0B", "Power In"),
        ("J2: PT-101 Pressure (150Ω 0.05%)", CYAN, "3.0V drop"),
        ("J3: TT-101 Header Temp (150Ω)", EMERALD, "3.0V drop"),
        ("J4: TT-102 Flue Gas Temp (150Ω)", CRIMSON, "3.0V drop"),
        ("J5: FT-101 Steam Flow (150Ω)", AMBER, "3.0V drop"),
        ("J6: AT-101 Blowdown TDS Shunt", INDIGO, "Analog In"),
    ]

    for idx, (lbl, col, note) in enumerate(term_labels):
        y_pos = 4.40 - idx * 0.48
        t_box = patches.FancyBboxPatch((5.45, y_pos - 0.17), 3.7, 0.38, boxstyle="round,pad=0.05", facecolor="#1E293B", edgecolor=col, linewidth=1.1)
        ax.add_patch(t_box)
        ax.text(5.60, y_pos, lbl, color=col, fontsize=8.6, fontweight="bold", va="center")
        ax.text(9.00, y_pos, note, color=MUTED_TEXT, fontsize=8.0, va="center", ha="right")

    # Retrofit Highlight Callout Card inside Zone 2
    retrofit_badge = patches.FancyBboxPatch((5.4, 0.62), 3.8, 0.62, boxstyle="round,pad=0.08", facecolor="#064E3B", edgecolor=EMERALD, linewidth=1.5)
    ax.add_patch(retrofit_badge)
    ax.text(7.3, 1.00, "★ ZERO PRESSURE VESSEL CUTTING ★", color="#A7F3D0", fontsize=10.5, fontweight="bold", ha="center", va="center")
    ax.text(7.3, 0.76, "Non-Intrusive Pass-Through | < 45-Min Install | Zero IBR De-rating", color="#E2E8F0", fontsize=8.8, ha="center", va="center")

    # Connecting wires from Boiler Sensors to TapasShield Phoenix Terminals
    for idx in range(5):
        y_src = sensors[idx]["y"]
        y_dst = 4.40 - (idx + 1) * 0.48
        col = sensors[idx]["color"]
        ax.annotate('', xy=(5.45, y_dst), xytext=(4.4, y_src),
                    arrowprops=dict(edgecolor=col, arrowstyle="->", lw=1.8, linestyle="--"),
                    zorder=6)

    # -------------------------------------------------------------
    # ZONE 3: DUAL CLOUD STREAM (RIGHT)
    # -------------------------------------------------------------
    zone3_box = patches.FancyBboxPatch((10.0, 0.5), 3.6, 6.1, boxstyle="round,pad=0.15", facecolor=CARD_BG, edgecolor=CYAN, linewidth=1.5)
    ax.add_patch(zone3_box)
    ax.text(10.2, 6.20, "ZONE 3: DUAL CLOUD REPUTATION", color=CYAN, fontsize=12.5, fontweight="bold")
    ax.text(10.2, 5.90, "Secured 4G LTE / Wi-Fi Uplink (1 Hz)", color=MUTED_TEXT, fontsize=9.5)

    # Cloud Uplink Icon / Modem
    modem_box = patches.FancyBboxPatch((10.3, 4.85), 3.0, 0.95, boxstyle="round,pad=0.1", facecolor="#1E293B", edgecolor=CYAN, linewidth=1.2)
    ax.add_patch(modem_box)
    ax.text(11.8, 5.42, "4G LTE / Wi-Fi MQTTS / WSS", color=CYAN, fontsize=10.8, fontweight="bold", ha="center")
    ax.text(11.8, 5.08, "TLS 1.3 + NIST P-256 Silicon Signature", color=MUTED_TEXT, fontsize=9.0, ha="center")

    # Arrow from TapasShield node to Modem
    ax.annotate('', xy=(10.3, 5.32), xytext=(9.3, 4.75),
                arrowprops=dict(edgecolor=CYAN, arrowstyle="->", lw=2.4), zorder=7)

    # Stream 1: MSME Operator
    s1_box = patches.FancyBboxPatch((10.3, 2.85), 3.0, 1.80, boxstyle="round,pad=0.1", facecolor="#064E3B", edgecolor=EMERALD, linewidth=1.5)
    ax.add_patch(s1_box)
    ax.text(10.5, 4.35, "STREAM 1: MSME OPERATOR", color=EMERALD, fontsize=11.0, fontweight="bold")
    ax.text(10.5, 4.05, "• Plant SCADA & Real-time Gauges\n• IS 8753 Efficiency Optimization\n• Waterside Scale Predictor (₹/hr)\n• Condition-based Descaling Alerts", color=TEXT_COLOR, fontsize=9.2, va="top", linespacing=1.35)

    # Stream 2: Central & State Govt
    s2_box = patches.FancyBboxPatch((10.3, 0.65), 3.0, 2.00, boxstyle="round,pad=0.1", facecolor="#1E1B4B", edgecolor=INDIGO, linewidth=1.5)
    ax.add_patch(s2_box)
    ax.text(10.5, 2.35, "STREAM 2: STATUTORY GOVT", color="#A5B4FC", fontsize=11.0, fontweight="bold")
    ax.text(10.5, 2.05, "• Central Boilers Board (DPIIT)\n• State Directorate of Boilers\n• SHA-256 Tamper-Proof Audit Trail\n• Instant IBR Form-VI Green Channel\n• 14-Day Queue -> Instant Renewal", color=TEXT_COLOR, fontsize=9.0, va="top", linespacing=1.35)

    # Split arrows from modem to stream 1 and stream 2
    ax.annotate('', xy=(11.8, 4.65), xytext=(11.8, 4.85),
                arrowprops=dict(edgecolor=EMERALD, arrowstyle="->", lw=2.0), zorder=8)
    ax.annotate('', xy=(11.8, 2.65), xytext=(11.8, 2.85),
                arrowprops=dict(edgecolor=INDIGO, arrowstyle="->", lw=2.0), zorder=8)

    out_path = "presentation/assets/diagram_industrial_deployment.png"
    plt.tight_layout()
    plt.savefig(out_path, facecolor=DARK_BG, edgecolor="none", dpi=300)
    plt.close()
    print(f"[OK] Generated: {out_path}")

def generate_diagram_pcb_3d_annotated():
    print("[3/3] Generating Annotated 3D KiCad PCB Diagram (Dual-Column Clean Layout)...")
    pcb_src = "hardware/pcb_3d_iso.png"
    if not os.path.exists(pcb_src):
        print(f"[ERR] {pcb_src} not found")
        return

    # Load base 3D render
    pcb_img = Image.open(pcb_src).convert("RGBA")

    # Create figure with dark industrial frame
    fig, ax = plt.subplots(figsize=(15, 8.2), dpi=300)
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 8.2)
    ax.axis("off")

    # Place 3D PCB image in the CENTER
    # x = 3.6 to 11.4, y = 0.5 to 7.3
    ax.imshow(pcb_img, extent=[3.6, 11.4, 0.4, 7.3], zorder=1)

    # Header
    ax.text(0.5, 7.75, "TAPASSHIELD SIL-2 HARDWARE ENGINE: 42-COMPONENT KICAD 8 PCB", color=CYAN, fontsize=17, fontweight="bold")
    ax.text(0.5, 7.40, "120 × 90 mm 2-Layer FR4 | IEC 61508 SIL-2 & Indian Boiler Regulations 1950 (Rule 392 Compliant)", color=MUTED_TEXT, fontsize=11.5)

    # -------------------------------------------------------------------------
    # LEFT COLUMN: Power, Screw Terminals & Shunts (Targeting Left PCB Edge)
    # -------------------------------------------------------------------------
    left_cards = [
        {
            "num": "1",
            "title": "24V Power Bus & Buck Stage",
            "parts": "J1 Terminal + U4 TPS54302 + L1 + U5 AP2112K",
            "desc": "24V DC input -> 5V Buck -> 3.3V Low-Noise LDO.\nSurvives factory power brownouts & 1.5A surges.",
            "color": AMBER,
            "y": 4.9,
            "target": (5.2, 5.0)  # Top left power section
        },
        {
            "num": "2",
            "title": "5x 4–20 mA Screw Terminals",
            "parts": "J2–J6 Phoenix Contact 5.08mm Euroblocks",
            "desc": "Non-intrusive pass-through for PT-101, TT-101,\nTT-102, FT-101, AT-101 without pipe cutting.",
            "color": EMERALD,
            "y": 2.7,
            "target": (4.9, 3.2)  # Green terminal block row
        },
        {
            "num": "3",
            "title": "TVS Surge Clamps & 0.05% Shunts",
            "parts": "D1–D5 SMAJ28CA + R1–R5 150.0 Ω (0.05%)",
            "desc": "Ultra-precision Susumu shunts (25ppm/°C).\nMax 3.0V loop drop. Clamps ±4kV transients.",
            "color": CRIMSON,
            "y": 0.5,
            "target": (5.7, 3.2)  # Shunts and TVS diodes
        }
    ]

    for sub in left_cards:
        card = patches.FancyBboxPatch((0.4, sub["y"]), 3.5, 1.85, boxstyle="round,pad=0.08", facecolor=CARD_BG, edgecolor=sub["color"], linewidth=1.5, zorder=3)
        ax.add_patch(card)

        # Badge Number
        badge = patches.Circle((0.75, sub["y"] + 1.45), 0.25, facecolor=sub["color"], edgecolor="none", zorder=4)
        ax.add_patch(badge)
        ax.text(0.75, sub["y"] + 1.45, sub["num"], color=DARK_BG, fontsize=11.5, fontweight="bold", ha="center", va="center", zorder=5)

        # Title
        ax.text(1.15, sub["y"] + 1.45, sub["title"], color=sub["color"], fontsize=12.0, fontweight="bold", va="center", zorder=4)
        # Components
        ax.text(0.6, sub["y"] + 1.05, sub["parts"], color=TEXT_COLOR, fontsize=10.0, fontweight="bold", va="center", zorder=4)
        # Description
        ax.text(0.6, sub["y"] + 0.52, sub["desc"], color=MUTED_TEXT, fontsize=9.2, va="center", zorder=4)

        # Callout line from right side of card to target on PCB
        tgt_x, tgt_y = sub["target"]
        ax.annotate('', xy=(tgt_x, tgt_y), xytext=(3.9, sub["y"] + 0.95),
                    arrowprops=dict(edgecolor=sub["color"], arrowstyle="->", lw=1.8),
                    zorder=6)
        dot = patches.Circle((tgt_x, tgt_y), 0.10, facecolor=sub["color"], edgecolor=TEXT_COLOR, linewidth=1.2, zorder=7)
        ax.add_patch(dot)

    # -------------------------------------------------------------------------
    # RIGHT COLUMN: Microcontroller, ADC & Cryptography (Targeting Right PCB Area)
    # -------------------------------------------------------------------------
    right_cards = [
        {
            "num": "4",
            "title": "ESP32-S3 Dual-Core MCU (U1)",
            "parts": "ESP32-S3-WROOM-1 (240MHz Xtensa LX7)",
            "desc": "Directs 1 Hz dual cloud stream over Wi-Fi/4G.\nGPIO4 (ADC1_CH3) samples Ch 5 (AT-101 TDS).\nRuns FreeRTOS SIL-2 watchdog daemon.",
            "color": "#C084FC",
            "y": 4.9,
            "target": (8.8, 4.8)  # U1 ESP32
        },
        {
            "num": "5",
            "title": "16-Bit Precision ADC (U3)",
            "parts": "ADS1115 MSOP-10 + R6–R10 / C1–C5 Filters",
            "desc": "125 µV/LSB differential resolution over I2C.\nReads PT-101, TT-101, TT-102, FT-101 with\nanti-aliasing 15.9 kHz RC low-pass filters.",
            "color": CYAN,
            "y": 2.7,
            "target": (7.4, 4.2)  # U3 ADS1115
        },
        {
            "num": "6",
            "title": "Silicon Root-of-Trust (U2)",
            "parts": "ATECC608B SOIC-8 Crypto Element",
            "desc": "Tamper-proof private key in write-locked Slot 0.\nSigns canonical RFC 8785 JSON with ECDSA\nNIST P-256 for non-repudiable audit ledger.",
            "color": INDIGO,
            "y": 0.5,
            "target": (8.0, 3.4)  # U2 ATECC608B
        }
    ]

    for sub in right_cards:
        card = patches.FancyBboxPatch((11.1, sub["y"]), 3.5, 1.85, boxstyle="round,pad=0.08", facecolor=CARD_BG, edgecolor=sub["color"], linewidth=1.5, zorder=3)
        ax.add_patch(card)

        # Badge Number
        badge = patches.Circle((11.45, sub["y"] + 1.45), 0.25, facecolor=sub["color"], edgecolor="none", zorder=4)
        ax.add_patch(badge)
        ax.text(11.45, sub["y"] + 1.45, sub["num"], color=DARK_BG, fontsize=11.5, fontweight="bold", ha="center", va="center", zorder=5)

        # Title
        ax.text(11.85, sub["y"] + 1.45, sub["title"], color=sub["color"], fontsize=12.0, fontweight="bold", va="center", zorder=4)
        # Components
        ax.text(11.3, sub["y"] + 1.05, sub["parts"], color=TEXT_COLOR, fontsize=10.0, fontweight="bold", va="center", zorder=4)
        # Description
        ax.text(11.3, sub["y"] + 0.52, sub["desc"], color=MUTED_TEXT, fontsize=9.2, va="center", zorder=4)

        # Callout line from left side of card to target on PCB
        tgt_x, tgt_y = sub["target"]
        ax.annotate('', xy=(tgt_x, tgt_y), xytext=(11.1, sub["y"] + 0.95),
                    arrowprops=dict(edgecolor=sub["color"], arrowstyle="->", lw=1.8),
                    zorder=6)
        dot = patches.Circle((tgt_x, tgt_y), 0.10, facecolor=sub["color"], edgecolor=TEXT_COLOR, linewidth=1.2, zorder=7)
        ax.add_patch(dot)

    out_path = "presentation/assets/diagram_pcb_3d_annotated.png"
    plt.tight_layout()
    plt.savefig(out_path, facecolor=DARK_BG, edgecolor="none", dpi=300)
    plt.close()
    print(f"[OK] Generated: {out_path}")

if __name__ == "__main__":
    generate_crops()
    generate_diagram_industrial_deployment()
    generate_diagram_pcb_3d_annotated()
