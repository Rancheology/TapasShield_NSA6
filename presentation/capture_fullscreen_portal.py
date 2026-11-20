import os
import sys
import time
import subprocess
import urllib.request
import json
from playwright.sync_api import sync_playwright

root_dir = os.path.abspath(".")
visual_assets_dir = os.path.join(root_dir, "presentation", "visual_guide_assets")
os.makedirs(visual_assets_dir, exist_ok=True)

print("Starting Uvicorn backend server on 127.0.0.1:8000...")
server_process = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"],
    cwd=root_dir,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

try:
    # Wait for server to be responsive
    for i in range(25):
        try:
            req = urllib.request.urlopen("http://127.0.0.1:8000/api/status", timeout=1)
            if req.status == 200:
                print("Backend server is live and responding!")
                break
        except Exception:
            time.sleep(0.5)
    else:
        raise RuntimeError("Backend server failed to start within 12 seconds!")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1600, "height": 900},
            device_scale_factor=2
        )
        page = context.new_page()
        page.goto("http://127.0.0.1:8000/", wait_until="networkidle")
        time.sleep(1)

        # ---------------------------------------------------------
        # SHOT A: Full Business Portal (MSME Operator)
        # ---------------------------------------------------------
        print("\n--- Capturing Shot A: Full Business Portal ---")
        # Click 1. Business Portal (MSME Operator)
        page.locator('button:has-text("1. Business Portal (MSME Operator)")').click()
        time.sleep(0.5)

        # Click 2. Scale Buildup (100x)
        page.locator('button:has-text("2. Scale Buildup (100x)")').click()
        print("Waiting 3.5 seconds for scale drift and live fuel loss...")
        time.sleep(3.5)

        # Adjust zoom slightly to 0.82 to capture all 4 zones in 1600x900 frame
        page.evaluate('document.body.style.zoom = "0.82"')
        time.sleep(0.6)

        shot_a_path = os.path.join(visual_assets_dir, "portal_full_business.png")
        page.screenshot(path=shot_a_path)
        print(f"Saved Shot A: {shot_a_path} ({os.path.getsize(shot_a_path)/1024:.1f} KB)")

        # Compute normalized bounding boxes for Pins 1-4 using locator.bounding_box()
        # Viewport is 1600x900
        vw = 1600.0
        vh = 900.0

        def get_coords(loc, default_x, default_y):
            try:
                if loc.count() > 0:
                    box = loc.first.bounding_box()
                    if box:
                        cx = (box['x'] + box['width'] * 0.5) / vw * 100
                        cy = (box['y'] + box['height'] * 0.5) / vh * 100
                        return {"x": round(cx, 1), "y": round(cy, 1), "box": box}
            except Exception as e:
                print(f"Bounding box query error: {e}")
            return {"x": default_x, "y": default_y, "box": None}

        # Pin 1: Live Scenario & Role Bar (top)
        pin1 = get_coords(page.locator('text=STAKEHOLDER ROLE SWITCHER'), 50.0, 14.0)
        # Pin 2: Animated SVG Boiler Twin
        pin2 = get_coords(page.locator('svg').first, 45.0, 36.0)
        # Pin 3: IS 8753 Efficiency / Fuel Waste
        pin3 = get_coords(page.locator('text=NET FUEL COST PENALTY').first, 30.0, 72.0)
        # Pin 4: Loop Current Monitor
        pin4 = get_coords(page.locator('text=4-20 mA SENSOR LOOP CURRENT').first, 75.0, 72.0)

        boxes_a = {
            "pin1_controls": pin1,
            "pin2_boiler_twin": pin2,
            "pin3_fuel_loss": pin3,
            "pin4_loops": pin4
        }
        print("Computed Pins 1-4 normalized coords (%):", json.dumps(boxes_a, indent=2))

        # ---------------------------------------------------------
        # SHOT C: Tight non-letterboxed crop of top Jury Control Bar + Role Switcher
        # ---------------------------------------------------------
        print("\n--- Capturing Shot C: Tight non-letterboxed Control Bar ---")
        page.evaluate('document.body.style.zoom = "1.0"')
        time.sleep(0.3)
        # We can take a screenshot of the top controls container (Jury bar + header + role switcher)
        shot_c_path = os.path.join(visual_assets_dir, "portal_zoom_controls.png")
        page.screenshot(path=shot_c_path, clip={"x": 0, "y": 0, "width": 1600, "height": 190})
        print(f"Saved Shot C: {shot_c_path} ({os.path.getsize(shot_c_path)/1024:.1f} KB)")

        # ---------------------------------------------------------
        # SHOT B: Full Govt Inspector Portal (Accurately Scrolled)
        # ---------------------------------------------------------
        print("\n--- Capturing Shot B: Full Govt Inspector Portal ---")
        # Click 2. State & Central Govt Inspector Portal
        page.locator('button:has-text("2. State & Central Govt Inspector Portal")').click()
        time.sleep(0.5)

        # Click 5. Spoof & DB Tamper
        page.locator('button:has-text("5. Spoof & DB Tamper")').click()
        time.sleep(1.0)

        # Click Run Forensic Audit
        page.locator('button:has-text("Run Forensic Audit")').click()
        print("Waiting 2.5 seconds for audit report to render...")
        time.sleep(2.5)

        # Adjust zoom slightly to 0.85 so toolbar, crimson alert, 4 metadata cards AND cluster grid all fit in 900px
        page.evaluate('document.body.style.zoom = "0.85"')
        time.sleep(0.3)

        # Scroll GovtInspectorView directly into view so Boiler P&ID is not shown
        page.evaluate("""() => {
            const h2 = Array.from(document.querySelectorAll('h2')).find(el => el.textContent.includes('Central Boilers Board'));
            if (h2) {
                const card = h2.closest('.rounded-xl') || h2;
                card.scrollIntoView({ block: 'start', behavior: 'instant' });
                window.scrollBy(0, -10); // slight top margin
            }
        }""")
        time.sleep(0.5)

        shot_b_path = os.path.join(visual_assets_dir, "portal_full_inspector.png")
        page.screenshot(path=shot_b_path)
        print(f"Saved Shot B: {shot_b_path} ({os.path.getsize(shot_b_path)/1024:.1f} KB)")

        # Compute normalized bounding boxes for Pins 5-8
        # Pin 5: Forensic Audit & Certificate toolbar
        pin5 = get_coords(page.locator('button:has-text("Run Forensic Audit")').first, 80.0, 7.0)
        # Pin 6: Broken SHA-256 Hash Alert
        pin6 = get_coords(page.locator('text=Tampered Block: Sequence').first, 50.0, 22.0)
        # Pin 7: Hardware SIL Status
        pin7 = get_coords(page.locator('text=HARDWARE SIL CHIP').first, 38.0, 36.0)
        # Pin 8: Central Govt National Cluster Grid
        pin8 = get_coords(page.locator('text=Central Govt (DPIIT) National Industrial Cluster Grid').first, 50.0, 65.0)

        boxes_b = {
            "pin5_toolbar": pin5,
            "pin6_tamper_alert": pin6,
            "pin7_sil_status": pin7,
            "pin8_national_grid": pin8
        }
        print("Computed Pins 5-8 normalized coords (%):", json.dumps(boxes_b, indent=2))

        # ---------------------------------------------------------
        # SHOT D: Tight crop of Forensic Hash-Chain Audit & Digital Form-VI Certificate block
        # ---------------------------------------------------------
        print("\n--- Capturing Shot D: Tight crop of Forensic Audit & Cert block ---")
        shot_d_path = os.path.join(visual_assets_dir, "portal_zoom_audit_cert.png")
        # Screenshot the top inspector card element directly
        inspector_card = page.locator('div.rounded-xl:has(h2:has-text("Central Boilers Board"))').first
        if inspector_card.count() > 0:
            inspector_card.screenshot(path=shot_d_path)
            print(f"Saved Shot D via element locator: {shot_d_path} ({os.path.getsize(shot_d_path)/1024:.1f} KB)")
        else:
            page.screenshot(path=shot_d_path, clip={"x": 50, "y": 20, "width": 1500, "height": 450})
            print(f"Saved Shot D via clip fallback: {shot_d_path} ({os.path.getsize(shot_d_path)/1024:.1f} KB)")

        # Save coordinates to a JSON file for reference
        coords_file = os.path.join(visual_assets_dir, "portal_pin_coordinates.json")
        with open(coords_file, "w") as f:
            json.dump({"business_pins": boxes_a, "inspector_pins": boxes_b}, f, indent=2)
        print(f"Saved pin coordinates to {coords_file}")

        browser.close()

finally:
    print("\nTerminating Uvicorn backend process...")
    server_process.terminate()
    try:
        server_process.wait(timeout=3)
    except Exception:
        server_process.kill()
    print("Backend process cleanly terminated.")
