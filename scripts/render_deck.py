#!/usr/bin/env python3
"""
TapasShield NSA 6.0 Playwright Deck Renderer
Renders presentation/deck_html/index.html into:
1. presentation/TapasShield_NSA6_Final_Deck.pdf (Vector 16:9 PDF)
2. presentation/audit_slides/slide_01.png ... slide_10.png (Retina 3200x1800 captures)
Strictly audits overflow, broken images, and dimensions.
"""

import os
import sys
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
import fitz  # PyMuPDF

HTML_PATH = Path("presentation/deck_html/index.html").resolve()
PDF_OUT = Path("presentation/TapasShield_NSA6_Final_Deck.pdf").resolve()
SLIDES_DIR = Path("presentation/audit_slides").resolve()
SLIDES_DIR.mkdir(parents=True, exist_ok=True)

async def render_and_audit():
    print(f"[1/4] Loading HTML deck from: {HTML_PATH}")
    if not HTML_PATH.exists():
        print(f"[ERROR] {HTML_PATH} does not exist!")
        sys.exit(1)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Device scale factor 2 for crisp 3200x1800 retina PNG screenshots
        context = await browser.new_context(
            viewport={"width": 1600, "height": 900},
            device_scale_factor=2
        )
        page = await context.new_page()

        file_url = HTML_PATH.as_uri()
        print(f"[2/4] Navigating to {file_url} ...")
        await page.goto(file_url, wait_until="networkidle")

        # Wait for all fonts and images to settle
        await page.wait_for_timeout(2000)

        # Audit each of the 10 slides
        print("[3/4] Running strict DOM geometry, layout & image audits across all 10 slides...")
        audit_errors = []

        for i in range(1, 11):
            slide_id = f"slide-{i}"
            slide_loc = page.locator(f"#{slide_id}")
            if await slide_loc.count() == 0:
                audit_errors.append(f"Missing #{slide_id} on page")
                continue

            # Evaluate DOM metrics inside Chromium
            metrics = await slide_loc.evaluate("""el => {
                const rect = el.getBoundingClientRect();
                const images = Array.from(el.querySelectorAll('img')).map(img => ({
                    src: img.src,
                    complete: img.complete,
                    naturalWidth: img.naturalWidth,
                    naturalHeight: img.naturalHeight
                }));
                return {
                    scrollWidth: el.scrollWidth,
                    scrollHeight: el.scrollHeight,
                    clientWidth: el.clientWidth,
                    clientHeight: el.clientHeight,
                    images: images
                };
            }""")

            # Check overflow
            sw = metrics["scrollWidth"]
            sh = metrics["scrollHeight"]
            cw = metrics["clientWidth"]
            ch = metrics["clientHeight"]

            if sw > 1600 or sh > 900:
                audit_errors.append(
                    f"Slide {i:02d} OVERFLOW: scrollWidth={sw} (max 1600), scrollHeight={sh} (max 900)"
                )

            # Check broken images
            for img_info in metrics["images"]:
                if not img_info["complete"] or img_info["naturalWidth"] == 0:
                    audit_errors.append(
                        f"Slide {i:02d} BROKEN IMAGE: {img_info['src']}"
                    )

            # Capture Retina PNG
            slide_png_path = SLIDES_DIR / f"slide_{i:02d}.png"
            await slide_loc.screenshot(path=str(slide_png_path))
            print(f"  -> Slide {i:02d}: {cw}x{ch}px (scroll: {sw}x{sh}px, images: {len(metrics['images'])}) -> Saved {slide_png_path.name}")

        if audit_errors:
            print("\n[CRITICAL AUDIT FAILURES]:")
            for err in audit_errors:
                print(f"  ❌ {err}")
            await browser.close()
            sys.exit(1)
        else:
            print("  ✅ All 10 slides passed DOM geometry & image integrity audits with 0 defects.")

        # Render True-Vector 16:9 PDF
        print(f"[4/4] Rendering vector PDF to: {PDF_OUT} ...")
        await page.pdf(
            path=str(PDF_OUT),
            width="1600px",
            height="900px",
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}
        )

        await browser.close()

    # Verify PDF with PyMuPDF
    pdf_doc = fitz.open(str(PDF_OUT))
    page_count = len(pdf_doc)
    pdf_size_mb = os.path.getsize(str(PDF_OUT)) / (1024 * 1024)
    print(f"\n[PDF VERIFICATION]:")
    print(f"  -> Page Count: {page_count} (Expected: 10)")
    print(f"  -> Dimensions: {pdf_doc[0].rect.width:.1f} x {pdf_doc[0].rect.height:.1f} pts")
    print(f"  -> File Size: {pdf_size_mb:.2f} MB (Limit: < 4.8 MB)")

    if page_count != 10:
        print(f"[ERROR] PDF page count {page_count} != 10")
        sys.exit(1)
    if pdf_size_mb >= 4.8:
        print(f"[ERROR] PDF size {pdf_size_mb:.2f} MB >= 4.8 MB")
        sys.exit(1)

    print(f"\n[SUCCESS] Vector PDF & Retina Slide PNGs rendered and verified perfectly!")

if __name__ == "__main__":
    asyncio.run(render_and_audit())

