#!/usr/bin/env python3
"""
Phase 1A: Live Product Screenshot Capture Script
Starts uvicorn backend.main:app on 127.0.0.1:8000, uses Playwright Chromium at 1600x900 (2x DPI)
to capture:
1. presentation/dynamic_assets/live_dual_register.png
2. presentation/dynamic_assets/live_scale_predictive.png
3. presentation/dynamic_assets/live_govt_tamper_audit.png
Then cleanly terminates uvicorn.
"""

import os
import sys
import time
import subprocess
import urllib.request
from playwright.sync_api import sync_playwright

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT_DIR, "presentation", "dynamic_assets")
os.makedirs(OUT_DIR, exist_ok=True)

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]


def wait_for_server(url: str, timeout: float = 20.0) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url, timeout=2.0) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            time.sleep(0.4)
    return False


def main():
    print("[PHASE 1A] Starting FastAPI + WebSocket server on 127.0.0.1:8000...")
    server_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=ROOT_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        if not wait_for_server("http://127.0.0.1:8000/api/status"):
            raise RuntimeError("FastAPI server failed to respond on http://127.0.0.1:8000/api/status")
        print("[PHASE 1A] Server ready! Launching Playwright Chromium (1600x900 @ 2x DPI)...")

        exec_path = None
        for c in CHROME_CANDIDATES:
            if os.path.exists(c):
                exec_path = c
                break

        with sync_playwright() as p:
            launch_kwargs = {"headless": True}
            if exec_path:
                launch_kwargs["executable_path"] = exec_path
            browser = p.chromium.launch(**launch_kwargs)
            context = browser.new_context(
                viewport={"width": 1600, "height": 900},
                device_scale_factor=2,
            )
            page = context.new_page()

            # 1. live_dual_register.png (Normal Verified State on Dual Split-Screen Portal)
            print("[1/3] Capturing live_dual_register.png (Normal Verified 12.0 bar)...")
            page.goto("http://127.0.0.1:8000", wait_until="networkidle")
            time.sleep(2.5)
            page.click("button:has-text('1. Normal (12 bar)')")
            time.sleep(2.0)
            p1 = os.path.join(OUT_DIR, "live_dual_register.png")
            page.screenshot(path=p1, full_page=False)
            print(f"      Saved: {p1} ({os.path.getsize(p1) // 1024} KB)")

            # 2. live_scale_predictive.png (Trigger Scale Buildup 100x Drift)
            print("[2/3] Triggering Scale Buildup (100x Drift) and waiting 3.5s...")
            page.click("button:has-text('2. Scale Buildup (100x)')")
            time.sleep(3.8)
            p2 = os.path.join(OUT_DIR, "live_scale_predictive.png")
            page.screenshot(path=p2, full_page=False)
            print(f"      Saved: {p2} ({os.path.getsize(p2) // 1024} KB)")

            # 3. live_govt_tamper_audit.png (Switch to Govt Inspector Portal, Spoof + DB Tamper + Forensic Audit)
            print("[3/3] Switching to State & Central Govt Inspector Portal + Spoof/Tamper + Forensic Audit...")
            page.click("button:has-text('2. State & Central Govt Inspector Portal')")
            time.sleep(1.2)
            page.click("button:has-text('5. Spoof & DB Tamper')")
            time.sleep(1.5)
            page.click("button:has-text('Run Forensic Audit')")
            time.sleep(1.8)
            p3 = os.path.join(OUT_DIR, "live_govt_tamper_audit.png")
            page.screenshot(path=p3, full_page=False)
            print(f"      Saved: {p3} ({os.path.getsize(p3) // 1024} KB)")

            # Reset before closing
            page.click("button:has-text('1. Normal (12 bar)')")
            time.sleep(0.5)
            browser.close()

        print("[PHASE 1A] All 3 live screenshots captured successfully!")
    finally:
        print("[PHASE 1A] Stopping background uvicorn server...")
        server_proc.terminate()
        try:
            server_proc.wait(timeout=5)
        except Exception:
            server_proc.kill()


if __name__ == "__main__":
    main()
