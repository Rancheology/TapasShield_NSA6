"""
Capture Multi-Angle PCB Photos & Zoomed UI Action Shots
For TapasShield Visual Hardware & Portal Guide (Slides 11-14).
"""

import os
import sys
import time
import urllib.request
import urllib.error
from PIL import Image, ImageChops, ImageEnhance
from playwright.sync_api import sync_playwright

def post_json(url):
    req = urllib.request.Request(url, data=b"{}", headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=3) as resp:
            return resp.read()
    except Exception as e:
        print(f"POST {url} failed: {e}")
        return None

def process_pcb_cutout(input_path, output_path, padding=20):
    im = Image.open(input_path).convert("RGBA")
    alpha = im.split()[3]
    bbox = alpha.getbbox()
    if bbox:
        x0 = max(0, bbox[0] - padding)
        y0 = max(0, bbox[1] - padding)
        x1 = min(im.width, bbox[2] + padding)
        y1 = min(im.height, bbox[3] + padding)
        cropped = im.crop((x0, y0, x1, y1))
    else:
        cropped = im
    cropped.save(output_path, "PNG", optimize=True)
    return cropped

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    guide_assets = os.path.join(root_dir, "presentation", "visual_guide_assets")
    html_visual_assets = os.path.join(root_dir, "presentation", "deck_html", "visual_assets")
    os.makedirs(guide_assets, exist_ok=True)
    os.makedirs(html_visual_assets, exist_ok=True)

    print("--- 1. Processing Multi-Angle & Macro PCB Photos ---")
    top_src = os.path.join(root_dir, "hardware", "pcb_3d_top.png")
    iso_src = os.path.join(root_dir, "hardware", "pcb_3d_iso.png")

    # 1. pcb_top_clean.png
    top_clean_path = os.path.join(guide_assets, "pcb_top_clean.png")
    im_top = process_pcb_cutout(top_src, top_clean_path, padding=25)
    print(f"Saved pcb_top_clean.png ({im_top.width}x{im_top.height})")

    # 2. pcb_iso_terminals.png
    iso_clean_path = os.path.join(guide_assets, "pcb_iso_terminals.png")
    im_iso = process_pcb_cutout(iso_src, iso_clean_path, padding=25)
    print(f"Saved pcb_iso_terminals.png ({im_iso.width}x{im_iso.height})")

    # 3. pcb_macro_terminals.png (Tight crop on left 35% of top PCB: J1..J6, D1..D5, R1..R5)
    macro_terminals_path = os.path.join(guide_assets, "pcb_macro_terminals.png")
    # Left ~35% width, vertically covering J1 to J6
    w, h = im_top.size
    box_terminals = (int(w * 0.05), int(h * 0.12), int(w * 0.36), int(h * 0.90))
    im_terminals = im_top.crop(box_terminals)
    im_terminals.save(macro_terminals_path, "PNG", optimize=True)
    print(f"Saved pcb_macro_terminals.png ({im_terminals.width}x{im_terminals.height})")

    # 4. pcb_macro_power_and_crypto.png (Crop on top power chain: J1, D6, U4, L1, U5, and U2)
    macro_power_path = os.path.join(guide_assets, "pcb_macro_power_and_crypto.png")
    box_power = (int(w * 0.12), int(h * 0.08), int(w * 0.58), int(h * 0.42))
    im_power = im_top.crop(box_power)
    im_power.save(macro_power_path, "PNG", optimize=True)
    print(f"Saved pcb_macro_power_and_crypto.png ({im_power.width}x{im_power.height})")

    # 5. pcb_macro_leds.png (Crop on SW1, R13/R14, LED1, LED2)
    macro_leds_path = os.path.join(guide_assets, "pcb_macro_leds.png")
    box_leds = (int(w * 0.38), int(h * 0.70), int(w * 0.65), int(h * 0.94))
    im_leds = im_top.crop(box_leds)
    im_leds.save(macro_leds_path, "PNG", optimize=True)
    print(f"Saved pcb_macro_leds.png ({im_leds.width}x{im_leds.height})")

    # 6. pcb_bottom_clean.png (Render bottom copper layer B.Cu via Playwright)
    b_cu_svg = os.path.join(root_dir, "hardware", "pcb_verified_svg", "tapasshield_edge-B_Cu.svg")
    bottom_clean_path = os.path.join(guide_assets, "pcb_bottom_clean.png")

    print("\n--- 2. Capturing Playwright Screenshots & Bottom PCB Render ---")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # A. Render Bottom PCB from B.Cu vector SVG
        b_page = browser.new_page(viewport={"width": 1200, "height": 900})
        # Read the raw SVG content and colorize copper/gold
        with open(b_cu_svg, "r") as f_svg:
            svg_content = f_svg.read()
        
        # Replace the KiCad blue B.Cu color with high-contrast gold ENIG copper pads and traces
        styled_svg = svg_content.replace("#4D7FC4", "#E5A93C").replace("#000000", "#144527")
        
        b_html = f"""
        <html>
        <body style="margin:0; padding:30px; background: transparent; display:flex; align-items:center; justify-content:center;">
          <div style="position:relative; width:920px; height:690px; background:#0B2314; border-radius:18px; border:3px solid #1A4D2E; box-shadow:0 25px 50px rgba(0,0,0,0.5); overflow:hidden; display:flex; align-items:center; justify-content:center;">
            <!-- M3 Corner Inset Holes with Gold Annular Rings -->
            <div style="position:absolute; top:28px; left:28px; width:32px; height:32px; border-radius:50%; background:#FAF9F6; border:5px solid #E5A93C; box-sizing:border-box;"></div>
            <div style="position:absolute; top:28px; right:28px; width:32px; height:32px; border-radius:50%; background:#FAF9F6; border:5px solid #E5A93C; box-sizing:border-box;"></div>
            <div style="position:absolute; bottom:28px; left:28px; width:32px; height:32px; border-radius:50%; background:#FAF9F6; border:5px solid #E5A93C; box-sizing:border-box;"></div>
            <div style="position:absolute; bottom:28px; right:28px; width:32px; height:32px; border-radius:50%; background:#FAF9F6; border:5px solid #E5A93C; box-sizing:border-box;"></div>
            
            <!-- Silkscreen White Text on Bottom -->
            <div style="position:absolute; top:42px; left:100px; color:#FFFFFF; font-family:'JetBrains Mono',monospace; font-size:15px; font-weight:700; letter-spacing:1px; opacity:0.9;">
              TAPASSHIELD EDGE SIL-2 • B.Cu GROUND PLANE
            </div>
            <div style="position:absolute; bottom:42px; right:100px; color:#FFFFFF; font-family:'JetBrains Mono',monospace; font-size:13px; font-weight:600; opacity:0.8;">
              MADE IN INDIA • 120×90mm 2-LAYER FR4 • REV 6.0
            </div>

            <!-- Vector B.Cu Copper Layer -->
            <div style="width:84%; height:84%; display:flex; align-items:center; justify-content:center;">
              {styled_svg}
            </div>
          </div>
        </body>
        </html>
        """
        b_page.set_content(b_html)
        b_page.wait_for_timeout(500)
        b_page.locator("div").first.screenshot(path=bottom_clean_path, omit_background=True)
        print(f"Saved pcb_bottom_clean.png ({bottom_clean_path})")

        # B. Capture Web Portal Views
        context = browser.new_context(
            viewport={"width": 1600, "height": 900},
            device_scale_factor=2
        )
        page = context.new_page()

        # Shot 1: Full Business MSME SCADA View
        print("Capturing ui_full_business.png...")
        post_json("http://127.0.0.1:8000/api/reset")
        post_json("http://127.0.0.1:8000/api/scenario/1")
        page.goto("http://127.0.0.1:8000/")
        page.wait_for_timeout(2000)
        btn_biz = page.locator('button:has-text("1. Business Portal (MSME Operator)")')
        if btn_biz.count() > 0:
            btn_biz.first.click()
        page.wait_for_timeout(2500)
        ui_biz_path = os.path.join(guide_assets, "ui_full_business.png")
        page.screenshot(path=ui_biz_path)
        print(f"Saved ui_full_business.png ({os.path.getsize(ui_biz_path)/1024:.1f} KB)")

        # Crop Step 1: Top 5-Scenario Control Bar & Role Switcher
        print("Capturing ui_crop_step1_scenarios.png...")
        ui_crop1_path = os.path.join(guide_assets, "ui_crop_step1_scenarios.png")
        # Header bar is at the top: y from 0 to 140
        im_biz = Image.open(ui_biz_path)
        # Scaled by 2
        w2, h2 = im_biz.size
        box_hdr = (0, 0, w2, int(h2 * 0.18))
        im_crop1 = im_biz.crop(box_hdr)
        im_crop1.save(ui_crop1_path, "PNG", optimize=True)
        print(f"Saved ui_crop_step1_scenarios.png ({im_crop1.width}x{im_crop1.height})")

        # Shot 2: Trigger Scale Buildup (100x Speed) & Crop Fuel/Scale Twin
        print("Capturing ui_crop_step2_scale_roi.png...")
        post_json("http://127.0.0.1:8000/api/scenario/2")
        page.wait_for_timeout(4000)
        scale_screen_path = os.path.join(guide_assets, "ui_scale_temp.png")
        page.screenshot(path=scale_screen_path)
        im_scale = Image.open(scale_screen_path)
        # Crop the boiler twin area + fuel metrics (approx y from 18% to 65%)
        box_scale = (int(w2 * 0.02), int(h2 * 0.16), int(w2 * 0.98), int(h2 * 0.68))
        im_crop2 = im_scale.crop(box_scale)
        ui_crop2_path = os.path.join(guide_assets, "ui_crop_step2_scale_roi.png")
        im_crop2.save(ui_crop2_path, "PNG", optimize=True)
        print(f"Saved ui_crop_step2_scale_roi.png ({im_crop2.width}x{im_crop2.height})")
        if os.path.exists(scale_screen_path):
            os.remove(scale_screen_path)

        # Shot 3: Full Inspector Portal
        print("Capturing ui_full_inspector.png...")
        post_json("http://127.0.0.1:8000/api/reset")
        post_json("http://127.0.0.1:8000/api/scenario/1")
        page.wait_for_timeout(1000)
        btn_gov = page.locator('button:has-text("2. State & Central Govt Inspector Portal")')
        if btn_gov.count() > 0:
            btn_gov.first.click()
        page.wait_for_timeout(2500)
        ui_insp_path = os.path.join(guide_assets, "ui_full_inspector.png")
        page.screenshot(path=ui_insp_path)
        print(f"Saved ui_full_inspector.png ({os.path.getsize(ui_insp_path)/1024:.1f} KB)")

        # Shot 4: Trigger Spoof & DB Tamper, Click Forensic Audit, Crop Alert & Chain
        print("Capturing ui_crop_step3_tamper_cert.png...")
        post_json("http://127.0.0.1:8000/api/scenario/5")
        page.wait_for_timeout(1000)
        btn_audit = page.locator('button:has-text("Run Forensic Audit")')
        if btn_audit.count() > 0:
            btn_audit.first.click()
        page.wait_for_timeout(2000)
        # Scroll down slightly so the crimson tamper alert and national grid are prominent
        page.evaluate("window.scrollBy(0, 160)")
        page.wait_for_timeout(1000)
        tamper_screen_path = os.path.join(guide_assets, "ui_tamper_temp.png")
        page.screenshot(path=tamper_screen_path)
        im_tamper = Image.open(tamper_screen_path)
        # Crop the alert area (approx y from 22% to 75%)
        box_tamper = (int(w2 * 0.02), int(h2 * 0.16), int(w2 * 0.98), int(h2 * 0.72))
        im_crop3 = im_tamper.crop(box_tamper)
        ui_crop3_path = os.path.join(guide_assets, "ui_crop_step3_tamper_cert.png")
        im_crop3.save(ui_crop3_path, "PNG", optimize=True)
        print(f"Saved ui_crop_step3_tamper_cert.png ({im_crop3.width}x{im_crop3.height})")
        if os.path.exists(tamper_screen_path):
            os.remove(tamper_screen_path)

        browser.close()

    # Mirror all generated assets into presentation/deck_html/visual_assets/
    print("\n--- 3. Mirroring Assets to deck_html/visual_assets/ ---")
    for fname in os.listdir(guide_assets):
        src = os.path.join(guide_assets, fname)
        dst = os.path.join(html_visual_assets, fname)
        if os.path.isfile(src):
            with open(src, "rb") as f_in, open(dst, "wb") as f_out:
                f_out.write(f_in.read())
            print(f"Mirrored {fname} ({os.path.getsize(dst)/1024:.1f} KB)")

    print("\n[SUCCESS] Visual Guide Assets Captured & Ready!")

if __name__ == "__main__":
    main()
