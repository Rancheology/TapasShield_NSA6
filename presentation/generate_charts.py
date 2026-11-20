import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = "presentation/assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

DARK_BG = "#0F172A"
PANEL_BG = "#131D31"
TEXT_COLOR = "#F8FAFC"
MUTED_TEXT = "#94A3B8"
EMERALD = "#10B981"
CYAN = "#38BDF8"
AMBER = "#F59E0B"
CRIMSON = "#EF4444"
INDIGO = "#818CF8"
GRID_COLOR = "#334155"

def set_dark_style(fig, axes):
    fig.patch.set_facecolor(DARK_BG)
    for ax in axes:
        ax.set_facecolor(PANEL_BG)
        ax.tick_params(colors=MUTED_TEXT, labelsize=10.5)
        ax.xaxis.label.set_color(TEXT_COLOR)
        ax.yaxis.label.set_color(TEXT_COLOR)
        ax.title.set_color(TEXT_COLOR)
        for spine in ax.spines.values():
            spine.set_color("#475569")
            spine.set_linewidth(1.0)
        ax.grid(True, linestyle="--", linewidth=0.5, color=GRID_COLOR, alpha=0.6)

def generate_chart_thermodynamic_drift():
    """Slide 6 - Waterside Scale Thickness vs Flue Stack Temp & Efficiency Penalty"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), dpi=300)
    set_dark_style(fig, [ax1, ax2])

    d_scale = np.linspace(0.0, 2.0, 100)
    t_sat = 187.965
    t_stack = t_sat + 32.0 + 38.5 * d_scale  # 219.965 -> 296.965 C

    # Left Subplot: Scale vs Stack Temp
    ax1.plot(d_scale, t_stack, color=AMBER, linewidth=2.8, label="Flue Stack Temp (T_stack)")
    ax1.axhline(y=t_sat, color=CYAN, linestyle=":", linewidth=1.8, label="T_sat (187.97°C @ 12 bar)")
    ax1.axhline(y=273.0, color=CRIMSON, linestyle="--", linewidth=2.0, label="Descaling Limit (273°C)")

    # Highlight critical region
    ax1.fill_between(d_scale, 273.0, t_stack, where=(t_stack >= 273.0), color=CRIMSON, alpha=0.25, label="High Risk Scale Zone")
    ax1.scatter([0.0, 1.38, 2.0], [220.0, 273.0, 297.0], color=[EMERALD, AMBER, CRIMSON], s=50, zorder=5)

    ax1.set_title("Waterside CaCO3 Scale vs. Flue Stack Drift", fontsize=13, fontweight="bold", pad=10)
    ax1.set_xlabel("Scale Thickness d_scale (mm)", fontsize=11.5, fontweight="bold")
    ax1.set_ylabel("Flue Gas Exit Temp (°C)", fontsize=11.5, fontweight="bold")
    ax1.set_ylim(180, 310)
    ax1.set_xlim(0.0, 2.0)
    ax1.legend(loc="upper left", fontsize=10, facecolor=DARK_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)

    # Right Subplot: Efficiency & Hourly Cost Penalty
    eff = 86.5 - 3.8 * d_scale  # 86.5% down to 78.9%
    loss_hr = (86.5 - eff) / 86.5 * 350 * 18 * 1.05  # Rs/hr

    ax2_cost = ax2.twinx()
    ax2_cost.set_facecolor(PANEL_BG)

    line1 = ax2.plot(d_scale, eff, color=CYAN, linewidth=2.6, label="IS 8753 Efficiency (%)")
    line2 = ax2_cost.plot(d_scale, loss_hr, color=CRIMSON, linewidth=2.6, linestyle="-.", label="Hourly Fuel Waste (₹/hr)")

    ax2.set_title("IS 8753 Indirect Efficiency & Fuel Penalty", fontsize=13, fontweight="bold", pad=10)
    ax2.set_xlabel("Scale Thickness d_scale (mm)", fontsize=11.5, fontweight="bold")
    ax2.set_ylabel("Boiler Efficiency (%)", color=CYAN, fontsize=11.5, fontweight="bold")
    ax2_cost.set_ylabel("Coal Cost Penalty (₹ / hr)", color=CRIMSON, fontsize=11.5, fontweight="bold")
    ax2.set_ylim(75, 90)
    ax2_cost.set_ylim(0, 650)
    ax2_cost.tick_params(colors=MUTED_TEXT, labelsize=10.5)
    for s in ax2_cost.spines.values():
        s.set_color("#475569")

    # Combined legend
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax2.legend(lines, labels, loc="lower left", fontsize=10, facecolor=DARK_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)

    # Annotation for annual loss
    ax2.text(0.95, 0.90, "At 2.0 mm Scale:\n-7.6% Thermal Eff.\n₹4.65 Lakh/yr Loss", 
             transform=ax2.transAxes, fontsize=11, fontweight="bold", verticalalignment='top', horizontalalignment='right',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#1E293B', edgecolor=AMBER, alpha=0.9), color=TEXT_COLOR)

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, "chart_thermodynamic_drift.png")
    plt.savefig(out_path, facecolor=DARK_BG, edgecolor="none", dpi=300)
    plt.close()
    print(f"[OK] Generated: {out_path}")

def generate_diagram_crypto_pipeline():
    """Slide 5 - 4-Stage Zero-Trust Anti-Falsification Pipeline Diagram"""
    fig, ax = plt.subplots(figsize=(11, 3.2), dpi=300)
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 3.2)
    ax.axis("off")

    stages = [
        {
            "num": "STAGE 1",
            "title": "5x 4-20mA AFE",
            "subtitle": "Passive Loop Sniffing",
            "desc": "150Ω 0.05% Shunts\nADS1115 16-bit ADC\n< 3.6 mA Wire-Cut Trap",
            "color": EMERALD,
            "x": 0.3, "w": 2.3
        },
        {
            "num": "STAGE 2",
            "title": "IAPWS-IF97",
            "subtitle": "Physics Cross-Check",
            "desc": "|T_steam - T_sat| ≤ 5°C\nVariance σ_P² > 0 check\nDefeats Resistor Spoof",
            "color": CYAN,
            "x": 3.0, "w": 2.3
        },
        {
            "num": "STAGE 3",
            "title": "ATECC608B Crypto",
            "subtitle": "Hardware Secure Element",
            "desc": "RFC 8785 Canonical JSON\nECDSA NIST P-256\nSHA-256 Hash Chain",
            "color": AMBER,
            "x": 5.7, "w": 2.3
        },
        {
            "num": "STAGE 4",
            "title": "Dual Cloud Split",
            "subtitle": "Zero-Trust Distribution",
            "desc": "Central/State e-Register\nMSME SCADA Cockpit\n100% Non-Repudiation",
            "color": INDIGO,
            "x": 8.4, "w": 2.3
        }
    ]

    for st in stages:
        rect = plt.Rectangle((st["x"], 0.2), st["w"], 2.8, facecolor=PANEL_BG, edgecolor=st["color"], linewidth=1.5, zorder=2)
        ax.add_patch(rect)
        hbar = plt.Rectangle((st["x"], 2.5), st["w"], 0.5, facecolor=st["color"], alpha=0.2, zorder=3)
        ax.add_patch(hbar)
        ax.text(st["x"] + 0.1, 2.7, st["num"], color=st["color"], fontsize=9.5, fontweight="bold", zorder=4)
        ax.text(st["x"] + st["w"]/2, 2.2, st["title"], color=TEXT_COLOR, fontsize=12.5, fontweight="bold", ha="center", zorder=4)
        ax.text(st["x"] + st["w"]/2, 1.85, st["subtitle"], color=st["color"], fontsize=10.0, fontstyle="italic", ha="center", zorder=4)
        ax.plot([st["x"] + 0.2, st["x"] + st["w"] - 0.2], [1.65, 1.65], color="#334155", linewidth=0.8, zorder=4)
        ax.text(st["x"] + 0.15, 1.45, st["desc"], color=MUTED_TEXT, fontsize=9.2, va="top", zorder=4, linespacing=1.35)

    for i in range(len(stages) - 1):
        x_start = stages[i]["x"] + stages[i]["w"]
        x_end = stages[i+1]["x"]
        y_mid = 1.6
        ax.annotate('', xy=(x_end, y_mid), xytext=(x_start, y_mid),
                    arrowprops=dict(facecolor='#38BDF8', edgecolor='none', width=2.5, headwidth=7, headlength=7),
                    zorder=5)

    out_path = os.path.join(ASSETS_DIR, "diagram_crypto_pipeline.png")
    plt.tight_layout()
    plt.savefig(out_path, facecolor=DARK_BG, edgecolor="none", dpi=300)
    plt.close()
    print(f"[OK] Generated: {out_path}")

def generate_chart_afe_loop_calibration():
    """Slide 4 - ADS1115 16-bit ADC Transfer Curve & 4-20mA Precision AFE"""
    fig, ax = plt.subplots(figsize=(6.0, 4.2), dpi=300)
    set_dark_style(fig, [ax])

    i_ma = np.linspace(0.0, 24.0, 200)
    v_shunt = i_ma * 0.150  # 0 to 3.6V
    adc_counts = (v_shunt / 4.096) * 32767

    ax.axvspan(0.0, 3.6, color=CRIMSON, alpha=0.22, label="Wire-Cut Trap (0 - 3.6 mA)")
    ax.axvspan(4.0, 20.0, color=EMERALD, alpha=0.18, label="Active Telemetry (4 - 20 mA)")
    ax.axvspan(13.6, 24.0, color=AMBER, alpha=0.15, label="MAWP Overpressure (>15 bar)")

    ax.plot(i_ma, adc_counts, color=CYAN, linewidth=2.8, label="ADC Transfer Line")

    nom_i = 11.68
    nom_c = (nom_i * 0.150 / 4.096) * 32767
    ax.scatter([nom_i], [nom_c], color=EMERALD, s=70, zorder=5)
    ax.annotate("12.0 bar (11.68 mA)\n1.752 V = 14,015 counts", xy=(nom_i, nom_c), xytext=(nom_i - 5.5, nom_c + 4000),
                arrowprops=dict(facecolor=EMERALD, edgecolor='none', width=1.5, headwidth=5),
                fontsize=9.5, fontweight="bold", color=TEXT_COLOR,
                bbox=dict(boxstyle="round,pad=0.3", facecolor=PANEL_BG, edgecolor=EMERALD, alpha=0.9))

    ax.set_title("16-Bit ADS1115 AFE Loop Calibration Curve", fontsize=12.5, fontweight="bold", pad=8)
    ax.set_xlabel("Loop Current I_loop (mA)", fontsize=11, fontweight="bold")
    ax.set_ylabel("16-Bit ADC Counts (FSR ±4.096V)", fontsize=11, fontweight="bold")
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 26000)

    ax_v = ax.twinx()
    ax_v.set_ylim(0, 26000 * 4.096 / 32767)
    ax_v.set_ylabel("Shunt Voltage (V)", color=MUTED_TEXT, fontsize=11, fontweight="bold")
    ax_v.tick_params(colors=MUTED_TEXT, labelsize=10)
    for s in ax_v.spines.values():
        s.set_color("#475569")

    ax.legend(loc="upper left", fontsize=9.2, facecolor=DARK_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, "chart_afe_loop_calibration.png")
    plt.savefig(out_path, facecolor=DARK_BG, edgecolor="none", dpi=300)
    plt.close()
    print(f"[OK] Generated: {out_path}")

def generate_chart_bom_and_roi():
    """Slide 8 - Unit Economics, Retrofit Cost Comparison & 12-Month MSME Cashflow"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.4), dpi=300)
    set_dark_style(fig, [ax1, ax2])

    categories = ["Industrial PLC\nRetrofit", "Commercial Loggers\n(Honeywell/Testo)", "TapasShield\nEdge Kit"]
    costs = [185000, 45000, 9999]
    bar_colors = [CRIMSON, AMBER, EMERALD]

    bars = ax1.barh(categories, costs, color=bar_colors, height=0.55, edgecolor="#334155", linewidth=1.0)
    ax1.set_title("Capital Outlay Comparison per Boiler", fontsize=12.5, fontweight="bold", pad=8)
    ax1.set_xlabel("Total Installed Cost (₹ INR)", fontsize=11, fontweight="bold")
    ax1.set_xlim(0, 245000)

    for bar, cost in zip(bars, costs):
        ax1.text(bar.get_width() + 4000, bar.get_y() + bar.get_height()/2, f"₹{cost:,}", 
                 va="center", color=TEXT_COLOR, fontsize=10.5, fontweight="bold")

    ax1.text(0.52, 0.68, "TapasShield BOM: ₹5,420\nZero Pressure Part Cutting\nZero IBR Shutdown", 
             transform=ax1.transAxes, fontsize=10.0, fontweight="bold", va="center", ha="left",
             bbox=dict(boxstyle="round,pad=0.4", facecolor=DARK_BG, edgecolor=EMERALD, alpha=0.9), color=EMERALD)

    months = np.arange(0, 13)
    monthly_net = 37750
    cum_cashflow = np.zeros(13)
    cum_cashflow[0] = -9999
    for m in range(1, 13):
        cum_cashflow[m] = cum_cashflow[m-1] + monthly_net

    ax2.plot(months, cum_cashflow / 1000, color=EMERALD, linewidth=2.8, marker="o", markersize=5.0, label="Cumulative Net Savings")
    ax2.axhline(0, color="#64748B", linestyle="--", linewidth=1.0)

    payback_month = 9999 / monthly_net
    ax2.scatter([payback_month], [0], color=AMBER, s=90, zorder=5)
    ax2.annotate("Payback: 4.2 Weeks", xy=(payback_month, 0), xytext=(payback_month + 1.2, -45),
                arrowprops=dict(facecolor=AMBER, edgecolor='none', width=1.5, headwidth=5),
                fontsize=10.5, fontweight="bold", color=AMBER,
                bbox=dict(boxstyle="round,pad=0.3", facecolor=DARK_BG, edgecolor=AMBER, alpha=0.9))

    ax2.set_title("12-Month Cumulative MSME Net Savings (₹k)", fontsize=12.0, fontweight="bold", pad=8)
    ax2.set_xlabel("Operational Month", fontsize=11, fontweight="bold")
    ax2.set_ylabel("Net Cash Flow (₹ Thousands)", fontsize=11, fontweight="bold")
    ax2.set_xlim(0, 12)
    ax2.set_ylim(-60, 480)

    ax2.text(0.95, 0.40, "Year-1 Net Profit:\n+₹4,43,000 / boiler\n44x Capital Return",
             transform=ax2.transAxes, fontsize=10.5, fontweight="bold", va="top", ha="right",
             bbox=dict(boxstyle="round,pad=0.4", facecolor=DARK_BG, edgecolor=EMERALD, alpha=0.9), color=TEXT_COLOR)

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, "chart_bom_and_roi.png")
    plt.savefig(out_path, facecolor=DARK_BG, edgecolor="none", dpi=300)
    plt.close()
    print(f"[OK] Generated: {out_path}")


def generate_dual_portal_mockup():
    """Slide 7 - Publication-grade UI Mockup of the Dual-Access Online Register (Business + State + Central Govt)."""
    fig, ax = plt.subplots(figsize=(11.5, 4.4), dpi=300)
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(DARK_BG)
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 4.4)
    ax.axis("off")

    # ==========================
    # 1. LEFT WINDOW: MSME BUSINESS PORTAL
    # ==========================
    w_left = 5.2
    # Outer Window Box
    win_left = plt.Rectangle((0.2, 0.15), w_left, 4.1, facecolor="#0B1329", edgecolor=EMERALD, linewidth=1.8, zorder=2)
    ax.add_patch(win_left)
    # Titlebar
    tbar_left = plt.Rectangle((0.2, 3.85), w_left, 0.4, facecolor="#162544", zorder=3)
    ax.add_patch(tbar_left)
    # Window Dots
    ax.add_patch(plt.Circle((0.40, 4.05), 0.06, color="#EF4444", zorder=4))
    ax.add_patch(plt.Circle((0.55, 4.05), 0.06, color="#F59E0B", zorder=4))
    ax.add_patch(plt.Circle((0.70, 4.05), 0.06, color="#10B981", zorder=4))
    ax.text(0.90, 4.05, "MSME BUSINESS PORTAL — PLANT SCADA & ROI COCKPIT", color=TEXT_COLOR, fontsize=8.2, fontweight="bold", va="center", zorder=4)

    # Subtitle / Node ID
    ax.text(0.40, 3.65, "Boiler Node: IBR-TN-VEL-2026-0891 | Vellore Leather & Chemical Cluster", color=CYAN, fontsize=7.8, fontweight="bold", zorder=4)
    ax.text(0.40, 3.45, "5-Channel Passive Loop Sniffing AFE (150Ω Shunts + ADS1115 16-Bit SAR ADC)", color=MUTED_TEXT, fontsize=7.0, zorder=4)

    # Telemetry Strip Container
    telem_box = plt.Rectangle((0.35, 2.45), 4.9, 0.85, facecolor="#111C38", edgecolor="#334155", linewidth=1.0, zorder=3)
    ax.add_patch(telem_box)
    ax.text(0.45, 3.12, "LIVE CALIBRATED TELEMETRY (1 Hz HARDWARE STREAM):", color="#94A3B8", fontsize=6.8, fontweight="bold", zorder=4)
    ax.text(0.45, 2.85, "PT-101: 12.00 bar (11.68 mA)", color=CYAN, fontsize=7.6, fontweight="bold", zorder=4)
    ax.text(2.65, 2.85, "TT-101: 187.96°C (Sat Steam)", color=AMBER, fontsize=7.6, fontweight="bold", zorder=4)
    ax.text(0.45, 2.60, "TT-102: 248.50°C (Flue Stack)", color=AMBER, fontsize=7.6, fontweight="bold", zorder=4)
    ax.text(2.65, 2.60, "FT-101: 3,420 kg/h | AT-101: 2,150 ppm TDS", color=EMERALD, fontsize=7.6, fontweight="bold", zorder=4)

    # 3 ROI & Maintenance KPI Cards
    kpis = [
        {"title": "IS 8753 Efficiency", "val": "82.4%", "sub": "Optimal Combustion", "col": EMERALD, "x": 0.35},
        {"title": "Fuel Loss Ticker", "val": "₹312 / hr", "sub": "Excess Flue Heat", "col": AMBER, "x": 2.02},
        {"title": "Descaling RUL", "val": "14 Days", "sub": "0.82mm Scale Est.", "col": CYAN, "x": 3.70},
    ]
    for k in kpis:
        cbox = plt.Rectangle((k["x"], 1.35), 1.55, 0.95, facecolor="#111C38", edgecolor=k["col"], linewidth=1.2, zorder=3)
        ax.add_patch(cbox)
        ax.text(k["x"] + 0.775, 2.12, k["title"], color="#94A3B8", fontsize=6.8, fontweight="bold", ha="center", zorder=4)
        ax.text(k["x"] + 0.775, 1.75, k["val"], color=k["col"], fontsize=12.0, fontweight="bold", ha="center", zorder=4)
        ax.text(k["x"] + 0.775, 1.48, k["sub"], color=TEXT_COLOR, fontsize=6.6, ha="center", zorder=4)

    # Bottom SCADA Value Box
    val_box = plt.Rectangle((0.35, 0.28), 4.9, 0.92, facecolor="#0E1A33", edgecolor=EMERALD, linewidth=1.0, zorder=3)
    ax.add_patch(val_box)
    ax.text(0.45, 1.02, "★ MSME BUSINESS OPERATIONAL VALUE:", color=EMERALD, fontsize=7.2, fontweight="bold", zorder=4)
    ax.text(0.45, 0.80, "• Direct ₹4.65 Lakh annual fuel savings via real-time IS 8753 optimization.", color=TEXT_COLOR, fontsize=6.8, zorder=4)
    ax.text(0.45, 0.60, "• Waterside scale tube rupture prevention (14-day descaling alert).", color=TEXT_COLOR, fontsize=6.8, zorder=4)
    ax.text(0.45, 0.40, "• Non-intrusive 4-20mA tap: Zero steam cutting, Zero factory downtime.", color="#94A3B8", fontsize=6.8, zorder=4)

    # ==========================
    # 2. CENTER SECURE BRIDGE BADGE
    # ==========================
    bridge_box = plt.Rectangle((5.52, 1.05), 0.46, 2.4, facecolor="#1E293B", edgecolor="#38BDF8", linewidth=1.5, zorder=3)
    ax.add_patch(bridge_box)
    ax.text(5.75, 3.25, "mTLS", color=CYAN, fontsize=7.2, fontweight="bold", ha="center", zorder=4)
    ax.text(5.75, 2.95, "4G LTE", color=TEXT_COLOR, fontsize=7.0, fontweight="bold", ha="center", zorder=4)
    ax.text(5.75, 2.60, "ECDSA\nP-256", color=AMBER, fontsize=6.5, fontweight="bold", ha="center", zorder=4)
    ax.text(5.75, 2.10, "SHA-256\nChain", color=EMERALD, fontsize=6.5, fontweight="bold", ha="center", zorder=4)
    ax.text(5.75, 1.60, "Zero\nTrust", color=CYAN, fontsize=6.5, fontweight="bold", ha="center", zorder=4)
    ax.text(5.75, 1.20, "1 Hz", color="#94A3B8", fontsize=6.5, ha="center", zorder=4)

    # Dual arrows
    ax.annotate('', xy=(5.50, 2.25), xytext=(5.42, 2.25), arrowprops=dict(facecolor=CYAN, edgecolor='none', width=1.5, headwidth=4.5), zorder=5)
    ax.annotate('', xy=(6.00, 2.25), xytext=(6.08, 2.25), arrowprops=dict(facecolor=CYAN, edgecolor='none', width=1.5, headwidth=4.5), zorder=5)

    # ==========================
    # 3. RIGHT WINDOW: GOVT STATUTORY E-REGISTER
    # ==========================
    x_right = 6.1
    win_right = plt.Rectangle((x_right, 0.15), w_left, 4.1, facecolor="#0B1329", edgecolor=CYAN, linewidth=1.8, zorder=2)
    ax.add_patch(win_right)
    # Titlebar
    tbar_right = plt.Rectangle((x_right, 3.85), w_left, 0.4, facecolor="#162544", zorder=3)
    ax.add_patch(tbar_right)
    # Window Dots
    ax.add_patch(plt.Circle((x_right + 0.20, 4.05), 0.06, color="#EF4444", zorder=4))
    ax.add_patch(plt.Circle((x_right + 0.35, 4.05), 0.06, color="#F59E0B", zorder=4))
    ax.add_patch(plt.Circle((x_right + 0.50, 4.05), 0.06, color="#10B981", zorder=4))
    ax.text(x_right + 0.70, 4.05, "STATE & CENTRAL GOVT STATUTORY e-REGISTER (DPIIT / CBB)", color=TEXT_COLOR, fontsize=8.2, fontweight="bold", va="center", zorder=4)

    # Subtitle
    ax.text(x_right + 0.20, 3.65, "Central Boilers Board (DPIIT) & Directorate of Boilers, Tamil Nadu", color=EMERALD, fontsize=7.8, fontweight="bold", zorder=4)
    ax.text(x_right + 0.20, 3.45, "Indian Boiler Regulations 1950 Rule 392 Continuous Audit & Auto-Renewal", color=MUTED_TEXT, fontsize=7.0, zorder=4)

    # Form-VI Digital Certificate Seal Banner
    cert_banner = plt.Rectangle((x_right + 0.15, 2.80), 4.9, 0.55, facecolor="#064E3B", edgecolor=EMERALD, linewidth=1.3, zorder=3)
    ax.add_patch(cert_banner)
    ax.text(x_right + 0.25, 3.17, "★ IBR FORM-VI DIGITAL STATUTORY SEAL: APPROVED (REMOTE)", color="#6EE7B7", fontsize=7.4, fontweight="bold", zorder=4)
    ax.text(x_right + 0.25, 2.92, "EODB Metric: 14 Days Manual Visit Queue → 0 Sec Real-Time Continuous Audit", color=TEXT_COLOR, fontsize=6.8, zorder=4)

    # National Cluster Registry Mini Table
    table_box = plt.Rectangle((x_right + 0.15, 1.25), 4.9, 1.45, facecolor="#111C38", edgecolor="#334155", linewidth=1.0, zorder=3)
    ax.add_patch(table_box)
    ax.text(x_right + 0.25, 2.52, "NATIONAL BOILER SAFETY & COMPLIANCE GRID (DPIIT OVERSIGHT):", color="#94A3B8", fontsize=6.8, fontweight="bold", zorder=4)

    headers = "BOILER REG ID        CLUSTER/STATE      PRESS    EFF%   CRYPTO CHAIN   EODB STATUS"
    ax.text(x_right + 0.25, 2.30, headers, color="#64748B", fontsize=6.4, fontfamily="monospace", fontweight="bold", zorder=4)

    rows = [
        ("IBR-TN-VEL-2026-0891", "Vellore [TN]  ", "12.0 bar", "82.4%", "[VERIFIED]", "AUTO-COMPLIANT", EMERALD),
        ("IBR-TN-TPR-2026-0412", "Tiruppur [TN] ", " 9.8 bar", "84.1%", "[VERIFIED]", "AUTO-COMPLIANT", EMERALD),
        ("IBR-GJ-SUR-2026-1104", "Surat [GJ]    ", "13.1 bar", "81.9%", "[VERIFIED]", "AUTO-COMPLIANT", EMERALD),
        ("IBR-MH-PUN-2026-0925", "Pune [MH]     ", "10.4 bar", "83.5%", "[VERIFIED]", "AUTO-COMPLIANT", EMERALD),
    ]
    y_pos = 2.08
    for r in rows:
        row_str = f"{r[0]}  {r[1]} {r[2]}  {r[3]}   {r[4]}   {r[5]}"
        ax.text(x_right + 0.25, y_pos, row_str, color=r[6], fontsize=6.3, fontfamily="monospace", zorder=4)
        y_pos -= 0.19

    # Live Blockchain Stream & Anti-Tamper Badges
    chain_box = plt.Rectangle((x_right + 0.15, 0.28), 4.9, 0.88, facecolor="#0E1A33", edgecolor=CYAN, linewidth=1.0, zorder=3)
    ax.add_patch(chain_box)
    ax.text(x_right + 0.25, 0.98, "ZERO-TRUST ANTI-FALSIFICATION FORENSIC LEDGER:", color=CYAN, fontsize=7.2, fontweight="bold", zorder=4)
    ax.text(x_right + 0.25, 0.77, "Block #1042 [VERIFIED]  ──▶  Block #1043 [VERIFIED]  ──▶  Block #1044 [TIP]", color=TEXT_COLOR, fontsize=6.6, fontfamily="monospace", zorder=4)
    ax.text(x_right + 0.25, 0.57, "• Traps Armed: 0mA Wire Cut (<3.6mA) | Resistor Spoof (|T_steam-T_sat| > 5°C)", color="#CBD5E1", fontsize=6.6, zorder=4)
    ax.text(x_right + 0.25, 0.38, "• Instant Statutory Revocation: Hash Mismatch or MAWP Breach Revokes Form-VI", color="#FCA5A5", fontsize=6.6, zorder=4)

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, "portal_dual_register_ui.png")
    plt.savefig(out_path, facecolor=DARK_BG, edgecolor="none", dpi=300)
    plt.close()
    print(f"[OK] Generated: {out_path}")


if __name__ == "__main__":
    generate_chart_thermodynamic_drift()
    generate_diagram_crypto_pipeline()
    generate_chart_afe_loop_calibration()
    generate_chart_bom_and_roi()
    generate_dual_portal_mockup()


