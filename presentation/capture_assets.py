"""
Capture Real Live Portal Screenshots & Studio 3D PCB Cutouts
For National Startup Awards 6.0 (NSA 6.0) Presentation.
"""

import os
import sys
import time
import subprocess
import urllib.request
import urllib.error
from PIL import Image, ImageChops

def check_server_running(url="http://127.0.0.1:8000/"):
    try:
        with urllib.request.urlopen(url, timeout=2) as resp:
            return resp.getcode() == 200
    except Exception:
        return False

def post_json(url):
    req = urllib.request.Request(url, data=b"{}", headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=3) as resp:
            return resp.read()
    except Exception as e:
        print(f"POST {url} failed: {e}")
        return None

def process_pcb_cutout(input_path, output_path, padding=20):
    print(f"Processing PCB cutout: {input_path} -> {output_path}")
    im = Image.open(input_path).convert("RGBA")
    
    # Check if image has alpha
    alpha = im.split()[3]
    bbox = alpha.getbbox()
    if bbox:
        # Transparent cutout
        x0 = max(0, bbox[0] - padding)
        y0 = max(0, bbox[1] - padding)
        x1 = min(im.width, bbox[2] + padding)
        y1 = min(im.height, bbox[3] + padding)
        cropped = im.crop((x0, y0, x1, y1))
    else:
        # Flood fill or corner alpha keying
        corner = im.getpixel((0, 0))
        # Create mask
        bg = Image.new("RGBA", im.size, corner)
        diff = ImageChops.difference(im, bg)
        bbox = diff.getbbox()
        if bbox:
            x0 = max(0, bbox[0] - padding)
            y0 = max(0, bbox[1] - padding)
            x1 = min(im.width, bbox[2] + padding)
            y1 = min(im.height, bbox[3] + padding)
            cropped = im.crop((x0, y0, x1, y1))
        else:
            cropped = im

    # Save RGBA PNG
    cropped.save(output_path, "PNG", optimize=True)
    print(f"Saved {output_path} ({cropped.width}x{cropped.height}, {os.path.getsize(output_path)/1024:.1f} KB)")
    return cropped

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dynamic_assets = os.path.join(root_dir, "presentation", "dynamic_assets")
    html_assets = os.path.join(root_dir, "presentation", "deck_html", "assets")
    os.makedirs(dynamic_assets, exist_ok=True)
    os.makedirs(html_assets, exist_ok=True)

    # 1. Process Studio PCB Cutouts
    print("--- 1. Processing Studio 3D PCB Cutouts ---")
    iso_src = os.path.join(root_dir, "hardware", "pcb_3d_iso.png")
    top_src = os.path.join(root_dir, "hardware", "pcb_3d_top.png")
    
    iso_dest = os.path.join(dynamic_assets, "pcb_studio_iso.png")
    top_dest = os.path.join(dynamic_assets, "pcb_studio_top.png")
    
    if os.path.exists(iso_src):
        process_pcb_cutout(iso_src, iso_dest)
        # Also mirror to html_assets
        Image.open(iso_dest).save(os.path.join(html_assets, "pcb_studio_iso.png"))
    if os.path.exists(top_src):
        process_pcb_cutout(top_src, top_dest)
        Image.open(top_dest).save(os.path.join(html_assets, "pcb_studio_top.png"))

    # 2. Capture Real Web App Screenshots
    print("--- 2. Capturing Real Web App Screenshots ---")
    server_process = None
    if not check_server_running():
        print("Starting backend uvicorn server...")
        server_process = subprocess.Popen(
            ["conda", "run", "-n", "tapasshield-nsa6", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"],
            cwd=root_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        for _ in range(20):
            if check_server_running():
                break
            time.sleep(0.5)

    if not check_server_running():
        print("ERROR: Could not connect to backend server at http://127.0.0.1:8000/")
        sys.exit(1)

    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={"width": 1600, "height": 900},
                device_scale_factor=2,
            )
            page = context.new_page()

            # --- SHOT 1: Live Dual Register (Normal 12.0 bar) ---
            print("Capturing Shot 1: live_dual_register.png...")
            post_json("http://127.0.0.1:8000/api/reset")
            post_json("http://127.0.0.1:8000/api/scenario/1")
            page.goto("http://127.0.0.1:8000/")
            page.wait_for_timeout(3000)

            shot1_path = os.path.join(dynamic_assets, "live_dual_register.png")
            page.screenshot(path=shot1_path, full_page=False)
            print(f"Shot 1 saved: {shot1_path} ({os.path.getsize(shot1_path)/1024:.1f} KB)")

            # --- SHOT 2: Live Scale Predictive View ---
            print("Capturing Shot 2: live_scale_predictive.png...")
            # Switch to Tab: 1. Business Portal (MSME Operator)
            btn_biz = page.locator('button:has-text("1. Business Portal (MSME Operator)")')
            if btn_biz.count() > 0:
                btn_biz.first.click()
            # Trigger scenario 2
            post_json("http://127.0.0.1:8000/api/scenario/2")
            page.wait_for_timeout(4000)

            shot2_path = os.path.join(dynamic_assets, "live_scale_predictive.png")
            page.screenshot(path=shot2_path, full_page=False)
            print(f"Shot 2 saved: {shot2_path} ({os.path.getsize(shot2_path)/1024:.1f} KB)")

            # --- SHOT 3: Live Govt Tamper & Forensic Audit ---
            print("Capturing Shot 3: live_govt_tamper_audit.png...")
            # Trigger scenario 5 (Resistor Spoof & DB Tamper)
            post_json("http://127.0.0.1:8000/api/scenario/5")
            # Switch to Tab: 2. State & Central Govt Inspector Portal
            btn_gov = page.locator('button:has-text("2. State & Central Govt Inspector Portal")')
            if btn_gov.count() > 0:
                btn_gov.first.click()
            page.wait_for_timeout(1000)
            
            # Click "Run Forensic Audit"
            btn_audit = page.locator('button:has-text("Run Forensic Audit")')
            if btn_audit.count() > 0:
                btn_audit.first.click()
            page.wait_for_timeout(2000)

            # Scroll down slightly to make sure the broken hash chain / red tamper banner and national grid are prominent
            page.evaluate("window.scrollBy(0, 180)")
            page.wait_for_timeout(1000)

            shot3_path = os.path.join(dynamic_assets, "live_govt_tamper_audit.png")
            page.screenshot(path=shot3_path, full_page=False)
            print(f"Shot 3 saved: {shot3_path} ({os.path.getsize(shot3_path)/1024:.1f} KB)")

            # Also mirror all screenshots to presentation/deck_html/assets/
            for name in ["live_dual_register.png", "live_scale_predictive.png", "live_govt_tamper_audit.png"]:
                src = os.path.join(dynamic_assets, name)
                dst = os.path.join(html_assets, name)
                if os.path.exists(src):
                    with open(src, "rb") as f_in, open(dst, "wb") as f_out:
                        f_out.write(f_in.read())

            browser.close()

    finally:
        if server_process:
            print("Terminating spawned server process...")
            server_process.terminate()

    # Verify captured files
    for name in ["live_dual_register.png", "live_scale_predictive.png", "live_govt_tamper_audit.png", "pcb_studio_iso.png", "pcb_studio_top.png"]:
        p = os.path.join(dynamic_assets, name)
        assert os.path.exists(p), f"Asset {name} was not created!"
        sz = os.path.getsize(p)
        assert sz > 25 * 1024, f"Asset {name} is suspiciously small: {sz} bytes"
        print(f"Verified {name}: {sz/1024:.1f} KB")

    print("\n[SUCCESS] Phase 2 Asset Capture Completed Successfully!")

if __name__ == "__main__":
    main()
