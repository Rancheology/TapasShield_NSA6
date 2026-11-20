#!/usr/bin/env python3
"""
TapasShield Automated Website & UI Screenshot Capture Script
Uses Playwright with local Chrome to capture pixel-perfect, high-resolution
screenshots of the running TapasShield IIoT platform at http://localhost:8000.
"""

import os
import time
from playwright.sync_api import sync_playwright

OUTPUT_DIR = os.path.abspath("presentation/screenshots")
os.makedirs(OUTPUT_DIR, exist_ok=True)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(CHROME_PATH):
    CHROME_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def run_capture():
    print(f"[INFO] Launching Browser from: {CHROME_PATH}")
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        # Create full HD context (1920 x 1080) with high device scale factor for crisp text
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=1.5
        )
        page = context.new_page()

        print("[1/9] Navigating to http://localhost:8000 (Default: Dual Split-Screen Hero View)...")
        page.goto("http://localhost:8000", wait_until="networkidle")
        time.sleep(2.5)  # Allow WebSocket telemetry and SVG animation to settle

        # 1. Dual Split-Screen Hero View
        split_path = os.path.join(OUTPUT_DIR, "screenshot_hero_split.png")
        page.screenshot(path=split_path, full_page=False)
        print(f"[OK] Captured: {split_path}")

        # 2. P&ID Schematic Widget
        try:
            pid_elem = page.locator("div:has-text('P&ID DIGITAL TWIN: INDUSTRIAL FIRE-TUBE BOILER')").last
            if pid_elem:
                pid_path = os.path.join(OUTPUT_DIR, "screenshot_pid_schematic.png")
                pid_elem.screenshot(path=pid_path)
                print(f"[OK] Captured P&ID Schematic: {pid_path}")
        except Exception as e:
            print(f"[WARN] Failed P&ID capture: {e}")

        # 3. Switch to Tab: Business Portal (MSME Operator)
        print("[2/9] Switching to 1. Business Portal (MSME Operator)...")
        page.click("text='1. Business Portal (MSME Operator)'")
        time.sleep(1.5)
        scada_path = os.path.join(OUTPUT_DIR, "screenshot_plant_scada.png")
        page.screenshot(path=scada_path, full_page=False)
        print(f"[OK] Captured: {scada_path}")

        # 4. Loop Current Monitor Widget
        try:
            loop_mon = page.locator("div:has-text('Industrial 4–20 mA Current Loop & ADS1115 AFE Inspector')").last
            loop_path = os.path.join(OUTPUT_DIR, "screenshot_loop_current_monitor.png")
            loop_mon.screenshot(path=loop_path)
            print(f"[OK] Captured Loop Current Monitor: {loop_path}")
        except Exception as e:
            print(f"[WARN] Loop monitor capture: {e}")

        # 5. Switch to Tab: State & Central Govt Inspector Portal
        print("[3/9] Switching to 2. State & Central Govt Inspector Portal...")
        page.click("text='2. State & Central Govt Inspector Portal'")
        time.sleep(1.5)
        inspector_path = os.path.join(OUTPUT_DIR, "screenshot_govt_inspector.png")
        page.screenshot(path=inspector_path, full_page=False)
        print(f"[OK] Captured: {inspector_path}")

        # 6. Open Digital IBR Form-VI Certificate Modal
        print("[4/9] Opening Digital IBR Form-VI Certificate Modal...")
        page.click("text='View Digital IBR Form-VI'")
        time.sleep(1.2)
        cert_path = os.path.join(OUTPUT_DIR, "screenshot_form_vi_certificate.png")
        page.screenshot(path=cert_path, full_page=False)
        print(f"[OK] Captured: {cert_path}")

        # Close Modal
        page.click("text='Close Certificate'")
        time.sleep(0.8)

        # 7. Simulate DB Tamper & Run Forensic Audit
        print("[5/9] Simulating DB Tamper Attack & Forensic Audit...")
        page.click("text='Simulate DB Tamper Attack'")
        time.sleep(1.0)
        page.click("text='Run Forensic Audit'")
        time.sleep(1.5)
        tamper_path = os.path.join(OUTPUT_DIR, "screenshot_forensic_audit_tamper.png")
        page.screenshot(path=tamper_path, full_page=False)
        print(f"[OK] Captured: {tamper_path}")

        # Reset System back to clean state
        page.click("text='Reset System'")
        time.sleep(1.2)

        # 8. Switch to Tab: SIL-2 Hardware CAD
        print("[6/9] Switching to 3. SIL-2 Hardware CAD...")
        page.click("text='3. SIL-2 Hardware CAD'")
        time.sleep(1.5)
        cad_path = os.path.join(OUTPUT_DIR, "screenshot_hardware_cad.png")
        page.screenshot(path=cad_path, full_page=False)
        print(f"[OK] Captured: {cad_path}")

        # 9. Switch to Tab: NSA 6.0 Pitch Deck and capture current slides
        print("[7/9] Switching to 4. NSA 6.0 Pitch Deck...")
        page.click("text='4. NSA 6.0 Pitch Deck'")
        time.sleep(1.5)

        deck_dir = os.path.join(OUTPUT_DIR, "deck_current")
        os.makedirs(deck_dir, exist_ok=True)

        for s_idx in range(1, 11):
            slide_btn = page.locator(f"button:has-text('{s_idx}.')").first
            if slide_btn:
                slide_btn.click()
                time.sleep(0.6)
            s_path = os.path.join(deck_dir, f"slide_{s_idx}.png")
            page.screenshot(path=s_path, full_page=False)
            print(f"[OK] Captured Deck Slide {s_idx}: {s_path}")

        browser.close()
        print("\n[SUCCESS] All Live Website & Deck Screenshots Captured Successfully!")

if __name__ == "__main__":
    run_capture()
