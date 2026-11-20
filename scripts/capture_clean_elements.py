#!/usr/bin/env python3
import os
import time
from playwright.sync_api import sync_playwright

OUTPUT_DIR = os.path.abspath("presentation/screenshots")
os.makedirs(OUTPUT_DIR, exist_ok=True)
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def capture_clean():
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=1.5
        )
        page = context.new_page()
        page.goto("http://localhost:8000", wait_until="networkidle")
        time.sleep(2.0)

        # 1. Switch to CAD tab and scroll down to the 3D Viewer
        print("[1/3] Capturing Hardware CAD 3D Viewer...")
        page.click("text='3. SIL-2 Hardware CAD'")
        time.sleep(1.5)
        page.evaluate("() => window.scrollTo(0, 450)")
        time.sleep(1.0)
        cad_path = os.path.join(OUTPUT_DIR, "screenshot_hardware_cad_3d.png")
        page.screenshot(path=cad_path, full_page=False)
        print(f"[OK] Hardware CAD 3D: {cad_path}")

        # 2. Switch to Inspector Tab, trigger tamper & audit, scroll to alert
        print("[2/3] Capturing Tamper Alert with full hash strings...")
        page.click("text='2. State & Central Govt Inspector Portal'")
        time.sleep(1.2)
        page.click("text='Simulate DB Tamper Attack'")
        time.sleep(0.8)
        page.click("text='Run Forensic Audit'")
        time.sleep(1.5)
        page.evaluate("() => window.scrollTo(0, 600)")
        time.sleep(0.8)
        tamper_path = os.path.join(OUTPUT_DIR, "screenshot_forensic_tamper_alert.png")
        page.screenshot(path=tamper_path, full_page=False)
        print(f"[OK] Tamper Alert: {tamper_path}")

        # Reset system back
        page.click("text='Reset System'")
        time.sleep(1.0)

        browser.close()

if __name__ == "__main__":
    capture_clean()
