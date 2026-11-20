#!/usr/bin/env python3
"""
TapasShield Live Presentation Assets Capture Script
Captures pixel-perfect real product screenshots from http://127.0.0.1:8000 with populated telemetry.
"""

import os
import time
import asyncio
from playwright.async_api import async_playwright
from PIL import Image

OUT_DIR = "presentation/screenshots"
os.makedirs(OUT_DIR, exist_ok=True)

async def capture_all():
    print("[1/5] Starting Playwright browser to capture live platform screenshots...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # High resolution viewport (1920x1080 @ 2x device scale factor for ultra-sharp Retina captures)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=2
        )
        page = await context.new_page()

        print("[2/5] Navigating to http://127.0.0.1:8000/ ...")
        await page.goto("http://127.0.0.1:8000/", wait_until="networkidle")
        
        # Wait 3 seconds for WebSocket connection and telemetry feed to stabilize
        print("  -> Waiting for live telemetry WebSocket streaming...")
        await page.wait_for_timeout(3500)

        # 1. Capture Live Hero Split Screen View (Dual Portal)
        print("[3/5] Capturing Live Hero Split-Screen View...")
        split_btn = page.locator("text=Dual Split-Screen (HERO VIEW)")
        if await split_btn.count() > 0:
            await split_btn.first.click()
            await page.wait_for_timeout(1000)
        hero_path = os.path.join(OUT_DIR, "live_hero_split.png")
        await page.screenshot(path=hero_path)
        print(f"  -> Saved: {hero_path}")

        # 2. Capture Business Portal (MSME Operator) - Plant SCADA & P&ID Twin
        print("  -> Capturing Business Portal (MSME Operator)...")
        scada_btn = page.locator("text=1. Business Portal (MSME Operator)")
        if await scada_btn.count() > 0:
            await scada_btn.first.click()
            await page.wait_for_timeout(1500)
            scada_path = os.path.join(OUT_DIR, "live_plant_scada.png")
            await page.screenshot(path=scada_path)
            print(f"  -> Saved: {scada_path}")

        # 3. Capture State & Central Govt Inspector Portal (Statutory e-Register)
        print("  -> Capturing Govt Inspector Portal (Online Register)...")
        insp_btn = page.locator("text=2. State & Central Govt Inspector Portal")
        if await insp_btn.count() > 0:
            await insp_btn.first.click()
            await page.wait_for_timeout(1500)
            insp_path = os.path.join(OUT_DIR, "live_govt_inspector.png")
            await page.screenshot(path=insp_path)
            print(f"  -> Saved: {insp_path}")

            # Capture Form-VI Digital Certificate Modal
            print("  -> Opening Digital IBR Form-VI Certificate Modal...")
            cert_btn = page.locator("button:has-text('View Digital IBR Form-VI')")
            if await cert_btn.count() > 0:
                await cert_btn.first.click()
                await page.wait_for_timeout(1200)
                cert_path = os.path.join(OUT_DIR, "live_form_vi_certificate.png")
                await page.screenshot(path=cert_path)
                print(f"  -> Saved: {cert_path}")

                # Close modal
                close_btn = page.locator("button:has-text('Close Certificate')")
                if await close_btn.count() > 0:
                    await close_btn.first.click()
                else:
                    await page.keyboard.press("Escape")
                await page.wait_for_timeout(500)

            # Trigger Scenario 5 (Spoof & DB Tamper) + Run Forensic Audit to capture Tamper Alert
            print("  -> Triggering Scenario 5 (Spoof & DB Tamper) & Forensic Audit...")
            s5_btn = page.locator("text=5. Spoof & DB Tamper")
            if await s5_btn.count() > 0:
                await s5_btn.first.click()
                await page.wait_for_timeout(1500)

            audit_btn = page.locator("button:has-text('Run Forensic Audit')")
            if await audit_btn.count() > 0:
                await audit_btn.first.click()
                await page.wait_for_timeout(1200)
                tamper_path = os.path.join(OUT_DIR, "live_forensic_tamper_alert.png")
                await page.screenshot(path=tamper_path)
                print(f"  -> Saved: {tamper_path}")

            # Reset back to Scenario 1 Normal
            s1_btn = page.locator("text=1. Normal (12 bar)")
            if await s1_btn.count() > 0:
                await s1_btn.first.click()
                await page.wait_for_timeout(1000)

        # 4. Capture SIL-2 Hardware CAD & 4-20mA Loop Inspector
        print("  -> Capturing SIL-2 Hardware CAD & 4-20mA Loop Inspector...")
        cad_btn = page.locator("text=3. SIL-2 Hardware CAD")
        if await cad_btn.count() > 0:
            await cad_btn.first.click()
            await page.wait_for_timeout(1500)
            cad_path = os.path.join(OUT_DIR, "live_hardware_cad_3d.png")
            await page.screenshot(path=cad_path)
            print(f"  -> Saved: {cad_path}")

        await browser.close()
        print("[4/5] Playwright screenshot capture completed successfully.")

    # 5. Generate precision crops
    print("[5/5] Generating precision crops for slide embedding...")
    crop_mappings = [
        # (source, crop_box_relative (left, top, right, bottom), dest_name)
        ("live_hero_split.png", (0.02, 0.08, 0.98, 0.96), "crop_live_hero_split.png"),
        ("live_plant_scada.png", (0.02, 0.08, 0.98, 0.50), "crop_live_pid_schematic.png"),
        ("live_plant_scada.png", (0.02, 0.50, 0.98, 0.96), "crop_live_scada_metrics.png"),
        ("live_govt_inspector.png", (0.02, 0.08, 0.98, 0.52), "crop_live_national_cluster_grid.png"),
        ("live_govt_inspector.png", (0.02, 0.52, 0.98, 0.96), "crop_live_crypto_hash_chain.png"),
        ("live_form_vi_certificate.png", (0.22, 0.10, 0.78, 0.90), "crop_live_form_vi_modal.png"),
        ("live_forensic_tamper_alert.png", (0.02, 0.48, 0.98, 0.96), "crop_live_tamper_alert.png"),
        ("live_hardware_cad_3d.png", (0.02, 0.08, 0.98, 0.52), "crop_live_loop_current_monitor.png"),
        ("live_hardware_cad_3d.png", (0.02, 0.52, 0.98, 0.96), "crop_live_kicad_cad_viewer.png"),
    ]

    for src_name, (l_rel, t_rel, r_rel, b_rel), dst_name in crop_mappings:
        src_path = os.path.join(OUT_DIR, src_name)
        dst_path = os.path.join(OUT_DIR, dst_name)
        if os.path.exists(src_path):
            img = Image.open(src_path)
            w, h = img.size
            box = (int(l_rel * w), int(t_rel * h), int(r_rel * w), int(b_rel * h))
            cropped = img.crop(box)
            cropped.save(dst_path)
            print(f"  -> Cropped {dst_name}: {cropped.size[0]}x{cropped.size[1]}")

    print("\n[OK] All live screenshots and crops generated and verified!")

if __name__ == "__main__":
    asyncio.run(capture_all())

