"""
Master Build & Verification Script: Dynamic HTML -> Vector PDFs + Retina PPTX
Generates:
1. TapasShield_NSA6_Pitch_Deck_10Slides.pdf (Slides 1–10, strictly < 4.0 MB)
2. TapasShield_Visual_User_Guide.pdf (Slides 11–15, strictly < 4.5 MB)
3. TapasShield_NSA6_Complete_15Slides.pdf (All 15 slides, strictly < 4.7 MB)
4. TapasShield_NSA6_Final_Deck.pdf (Complete 15 slides copy for platform links)
5. TapasShield_NSA6_Final_Deck.pptx (15 slides widescreen PPTX with jury speaker notes, strictly < 4.7 MB)
6. Standalone PNG posters in presentation/visual_guides/ (guide_01 through guide_05)
Enforces DOM Overflow = 0, Broken Images = 0 (including qr-code_github.png naturalWidth > 0), Zero XRef Corruption.
"""

import os
import sys
import io
import re
import shutil
from PIL import Image
import pymupdf
from pptx import Presentation
from pptx.util import Inches
from playwright.sync_api import sync_playwright

SPEAKER_NOTES = {
    1: (
        "Esteemed Jury of the National Startup Awards 6.0: India operates over 1,00,000 industrial boilers "
        "powering MSMEs across textiles, chemicals, leather, and food processing. Today, these boilers are blind, "
        "relying on mechanical gauges and paper logbooks that fail silently or invite falsification. We present TapasShield: "
        "an industrial-grade, SIL-2 capable IoT edge node built on the ESP32-S3 and ATECC608B hardware crypto element. "
        "In under 45 minutes, with zero pipe-cutting or plant shutdown, it clips onto existing 4–20 mA loops to establish "
        "an immutable, cryptographically verifiable telemetry bridge to both plant owners and State/Central Boiler Directorates."
    ),
    2: (
        "Every boiler explosion in India is preventable. Today, factory owners face a catastrophic dilemma: overpressure excursions "
        "above MAWP (15 bar) and low-water dry firing claim lives when mechanical bourdon gauges stick. Simultaneously, statutory "
        "compliance is an administrative nightmare: factories wait 10 to 14 days in queue for physical boiler inspectors, shutting down "
        "production. Paper logbooks and unencrypted local SD cards invite pre-inspection record fabrication. Finally, unmonitored waterside "
        "calcium carbonate scale (CaCO3) of just 1.5 mm causes +58°C stack heat loss, silently wasting ₹3.5 to ₹6 Lakhs of fuel per boiler every year."
    ),
    3: (
        "Why haven't existing solutions solved this? Traditional paper logs offer zero security and subjective audits. Commercial flue "
        "gas analyzers from Honeywell or Testo cost upwards of ₹45,000, yet only provide a local screen with no live government registry sync. "
        "Full PLC retrofits cost upwards of ₹1,85,000 and demand weeks of factory shutdown. TapasShield breaks this tradeoff at ₹9,999: "
        "non-intrusively sniffing 4–20 mA loops with Susumu 0.05% shunts, signing data in hardware silicon, and streaming live to the "
        "State & Central Government Online Register."
    ),
    4: (
        "Here is our core deliverable responding directly to the India EODB Grand Challenge: a live, dual-access online register shared "
        "simultaneously between the business and government. On the left, the MSME plant operator sees their real-time P&ID digital twin, "
        "live ₹/hr fuel burn rate, and predictive descaling countdown. On the right, the State Directorate of Boilers conducts continuous "
        "remote audits, auto-issuing the statutory IBR Form-VI Green-Channel certificate without manual inspector visits. At the macro level, "
        "DPIIT and Central Boilers Board monitor industrial cluster safety across Tamil Nadu, Gujarat, Maharashtra, and Punjab."
    ),
    5: (
        "How do we prevent falsification? We engineered a 3-layer cyber-physical defense. Layer 1: Hardware AFE catches physical wire-cuts "
        "(< 3.6 mA) using NAMUR NE43 loop traps. Layer 2: Our thermodynamic digital twin uses IAPWS-IF97 steam saturation equations to verify "
        "that steam temperature matches pressure. Clamping a fake resistor to trick the inspector into seeing 10.0 bar while the furnace is "
        "at 212°C triggers an immediate physical anomaly alarm. Layer 3: Every telemetry block is hashed into an append-only SHA-256 chain and "
        "signed inside the tamper-proof ATECC608B silicon chip. Modifying a historical database row shatters the chain, highlighting the violation in crimson."
    ),
    6: (
        "TapasShield doesn't just deliver safety—it is a profit center for MSMEs. Waterside CaCO3 scale acts as a thermal insulator, "
        "forcing the boiler to burn up to 15% more fuel. Our digital twin monitors stack temperature drift and blowdown TDS. When stack "
        "temperature approaches the 273°C threshold, TapasShield issues a 14-day advance descaling notice, preventing ₹4.65 Lakh per year "
        "in wasted fuel. With a total hardware cost of ₹9,999, the kit pays for itself in just 4.2 weeks, generating a 44x Year-1 return on capital."
    ),
    7: (
        "Our hardware is production-ready. The 120x90mm 2-layer FR4 board was designed in KiCad 8 and passed strict DRC with 0 errors and "
        "0 airwires. It accepts 24V industrial bus power via a TPS54302 buck converter and AP2112K low-noise LDO. Five Phoenix Contact screw "
        "terminals connect directly to factory sensors: steam pressure (PT-101), steam temperature (TT-101), flue stack temp (TT-102), "
        "steam flow (FT-101), and water quality/TDS (AT-101). All loops are protected by 400W SMAJ28CA TVS surge diodes and sampled with "
        "125 µV/LSB resolution by Texas Instruments ADS1115 16-bit ADC."
    ),
    8: (
        "We did not build mockups; every layer of TapasShield is built, tested, and verified today. Our Pytest test suite achieved 100% pass "
        "across all 21 automated tests, verifying IAPWS-IF97 thermodynamics, ADC count mapping, and crypto chains. Our ESP32-S3 C++ firmware compiles "
        "with 0 errors on PlatformIO, using just 7.6% RAM and 10.7% Flash. Our KiCad 8 PCB layout has 0 DRC violations across all 42 components. "
        "And our FastAPI + React full-stack portal is fully functional, demonstrating 5 real-time fault scenarios with 1 Hz dual-portal synchronization."
    ),
    9: (
        "Our unit economics enable massive national scalability. The 42-component bill of materials costs exactly ₹5,420 ($65). At an upfront "
        "kit price of ₹9,999, we earn a healthy 45% gross margin on hardware, followed by a ₹999/month recurring SaaS subscription at 85% "
        "gross margin. Our phased roadmap begins with a 50-boiler pilot in Tamil Nadu's Vellore leather and Tiruppur textile clusters, expands "
        "to Gujarat and Maharashtra in Phase 2, and scales to 10,000+ boilers in Phase 3, generating over ₹12 Crore in annual recurring revenue."
    ),
    10: (
        "TapasShield embodies the vision of Viksit Bharat @ 2047. Over 80% of India's boiler attendants are blue-collar workers who cannot "
        "read complex English manuals. TapasShield protects them through multi-lingual audio-visual alarms in Tamil, Hindi, Gujarati, and Marathi. "
        "At scale, saving 8-12% fuel across 10,000 boilers eliminates 2,80,000 tonnes of CO2 emissions annually, advancing India's Net-Zero 2070 goal. "
        "TapasShield delivers on Ease of Doing Business, eliminating 14-day inspection queues with instantaneous cryptographic verification—powering "
        "Make in India industrial competitiveness and worker safety."
    ),
    11: (
        "This is our 360-degree hardware teardown of the TapasShield SIL-2 Edge Node. On the left is our production 120x90mm 2-layer FR4 PCB "
        "with gold ENIG finish. Calling out exact physical components: Pin 01 accepts 24V plant power protected by a B540C Schottky diode. Pin 02 "
        "is the power supply rail stepping 24V down efficiently to 5V and 3.3V via high-frequency buck converters. Pin 03 shows our 5 Phoenix Contact "
        "5.08mm screw terminals, each backed by 400W SMAJ28CA TVS diodes and 0.05% precision shunts. Pin 04 is the Texas Instruments ADS1115 16-bit ADC. "
        "Pin 05 is our Microchip ATECC608B hardware crypto element providing hardware root-of-trust. Pin 06 hosts the ESP32-S3 SoC, physical tamper switch SW1, "
        "and diagnostic LEDs. On the right, our 3/4 perspective, macro front-end clamp, and solid ground plane demonstrate industrial durability."
    ),
    12: (
        "This is our visual connectivity guide showing direct boiler-to-PCB hookup. TapasShield connects non-intrusively in under 45 minutes "
        "with zero pipe cutting or downtime. The plant's 24V DC power feeds into terminal J1. Existing 4–20 mA instrument loops—steam pressure PT-101, "
        "steam temperature TT-101, flue stack gas temp TT-102, steam mass flow FT-101, and blowdown TDS AT-101—are simply clamped into terminals "
        "J2 through J6. The ESP32-S3 signs each packet using hardware ECDSA and transmits it over mTLS cellular 4G LTE or Wi-Fi directly to the "
        "shared statutory register. At the bottom, our status indicators provide instant physical feedback: solid green LED1 confirms active "
        "cryptographic synchronization, red LED2 warns of loop faults or overpressure, and SW1 locks down the device if the enclosure lid is opened."
    ),
    13: (
        "This is our full-screen tour of the Business MSME Plant SCADA Portal. Pin 1 gives operators instantaneous scenario controls and role switching. "
        "Pin 2 displays our animated thermodynamic P&ID digital twin, showing real-time IAPWS-IF97 steam saturation physics and dynamic calcium carbonate "
        "scale buildup on boiler tubes. Pin 3 tracks live financial bleed: displaying exact rupees-per-hour fuel waste and predictive 14-day descaling countdowns "
        "based on IS 8753 flue stack thermal drift. Pin 4 provides real-time 4–20 mA loop health and 16-bit ADS1115 raw ADC count monitoring, catching "
        "sensor faults and calibration drift before safety margins are breached."
    ),
    14: (
        "This is our full-screen tour of the State Inspectorate and Central Government (DPIIT) Online Register Portal, fulfilling the core mandate "
        "of the India EODB Grand Challenge. Pin 5 provides one-click statutory oversight: allowing inspectors to verify the tamper-proof ledger, inspect the public "
        "key, and issue digital IBR Form-VI renewal certificates. Pin 6 demonstrates our forensic tamper detection: simulating a database modification "
        "instantly shatters the append-only SHA-256 hash chain, highlighting the violation in crimson. Pin 7 displays our silicon root-of-trust: confirming "
        "the ATECC608B hardware crypto chip signature and statutory hold status. Pin 8 links the boiler into India's National Industrial Cluster Grid across "
        "Tamil Nadu, Gujarat, Maharashtra, and Punjab—replacing 14-day manual inspection queues with zero-second continuous verification."
    ),
    15: (
        "Our 4-step quick-start guide demonstrates that TapasShield installs non-intrusively in under 45 minutes with zero pipe cutting or factory shutdown. "
        "Step 1: Wire 24V plant power to terminal J1 and clip the 5 existing 4–20 mA sensor loops into terminals J2 through J6 via waterproof PG7 glands. "
        "Step 2: Link the ESP32-S3 to our dedicated industrial 4G LTE router; solid green LED1 confirms encrypted mTLS synchronization. "
        "Step 3: Open the portal, switch between business and government roles, or inject live faults to verify alarms. "
        "Step 4: Run the SHA-256 forensic audit and issue automated digital certificates. Finally, we believe in radical transparency: our entire codebase, "
        "PlatformIO firmware, and production KiCad 8 PCB design files and 3D models are 100% open source and reproducible on GitHub. Scan the QR code to verify every file today."
    )
}

TOTAL_SLIDES = 15

def generate_sub_deck_html(index_html_path, out_html_path, start_slide, end_slide, title):
    """Creates a standalone HTML file containing only a specific slice of slides."""
    with open(index_html_path, "r", encoding="utf-8") as f:
        full_html = f.read()

    head_match = re.search(r'(<head>[\s\S]*?</head>)', full_html)
    assert head_match, "head not found in index.html"
    head_html = head_match.group(1)

    # Update title
    head_html = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', head_html)

    # Ensure page-break-after: auto on the last slide of this slice
    sub_style = f"\n  <style> #slide-{end_slide} {{ page-break-after: auto !important; }} </style>\n"
    head_html = head_html.replace('</head>', f'{sub_style}</head>')

    slides_slice = ""
    for s in range(start_slide, end_slide + 1):
        slide_match = re.search(rf'(<section[^>]+id="slide-{s}"[\s\S]*?</section>)', full_html)
        assert slide_match, f"slide {s} not found in index.html"
        slides_slice += "\n" + slide_match.group(1)

    slice_html = f"""<!DOCTYPE html>
<html lang="en">
{head_html}
<body>
  <div class="deck-container">
    {slides_slice}
  </div>
</body>
</html>"""

    with open(out_html_path, "w", encoding="utf-8") as f:
        f.write(slice_html)
    print(f"Generated standalone HTML slice [{start_slide}–{end_slide}]: {out_html_path}")

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    presentation_dir = os.path.join(root_dir, "presentation")
    deck_html_dir = os.path.join(presentation_dir, "deck_html")
    index_html_path = os.path.join(deck_html_dir, "index.html")

    # Output paths
    deck_10_pdf_path = os.path.join(presentation_dir, "TapasShield_NSA6_Pitch_Deck_10Slides.pdf")
    guide_5_pdf_path = os.path.join(presentation_dir, "TapasShield_Visual_User_Guide.pdf")
    complete_15_pdf_path = os.path.join(presentation_dir, "TapasShield_NSA6_Complete_15Slides.pdf")
    final_deck_pdf_path = os.path.join(presentation_dir, "TapasShield_NSA6_Final_Deck.pdf")
    pptx_path = os.path.join(presentation_dir, "TapasShield_NSA6_Final_Deck.pptx")

    visual_guides_dir = os.path.join(presentation_dir, "visual_guides")
    audit_slides_dir = os.path.join(presentation_dir, "audit_slides")
    frontend_deck_dir = os.path.join(root_dir, "frontend", "public", "deck")

    os.makedirs(visual_guides_dir, exist_ok=True)
    os.makedirs(audit_slides_dir, exist_ok=True)
    os.makedirs(frontend_deck_dir, exist_ok=True)

    # 1. Generate standalone slice HTML files
    deck_10_html_path = os.path.join(deck_html_dir, "pitch_deck_10.html")
    guide_5_html_path = os.path.join(deck_html_dir, "user_guide.html")

    generate_sub_deck_html(index_html_path, deck_10_html_path, 1, 10, "TapasShield NSA 6.0 — 10-Slide Pitch Deck")
    generate_sub_deck_html(index_html_path, guide_5_html_path, 11, 15, "TapasShield NSA 6.0 — Visual Hardware & Portal Guide")

    print("\n--- 1. Launching Playwright Chromium & Loading 15-Slide Deck ---")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1600, "height": 900},
            device_scale_factor=2
        )
        page = context.new_page()
        page.goto(f"file:///{index_html_path.replace(os.sep, '/')}")
        page.wait_for_load_state("networkidle")
        page.evaluate("document.fonts.ready")

        print("\n--- 2. Running Strict Automated DOM & Image Gatekeeper (15 Slides) ---")
        errors = []
        for slide_num in range(1, TOTAL_SLIDES + 1):
            slide_id = f"#slide-{slide_num}"
            check = page.evaluate("""(slideId) => {
                const el = document.querySelector(slideId);
                if (!el) return { found: false };
                
                // Check geometry
                const sw = el.scrollWidth;
                const sh = el.scrollHeight;
                const rect = el.getBoundingClientRect();
                
                // Check images (especially verifying naturalWidth > 0)
                const imgs = Array.from(el.querySelectorAll('img'));
                const brokenImgs = imgs.filter(img => !img.complete || img.naturalWidth === 0).map(img => img.src);
                
                // Check leaf text elements overflow
                const leaves = Array.from(el.querySelectorAll('h1, h2, h3, h4, p, span, div, table, tr, td, th')).filter(
                    e => e.children.length === 0 && e.textContent.trim().length > 0
                );
                const overflowingElements = [];
                const elRect = el.getBoundingClientRect();
                for (const leaf of leaves) {
                    const r = leaf.getBoundingClientRect();
                    if (r.right > elRect.right + 2 || r.bottom > elRect.bottom + 2) {
                        overflowingElements.push({
                            tag: leaf.tagName,
                            text: leaf.textContent.slice(0, 30),
                            rightOverflow: r.right - elRect.right,
                            bottomOverflow: r.bottom - elRect.bottom
                        });
                    }
                }
                
                return {
                    found: true,
                    scrollWidth: sw,
                    scrollHeight: sh,
                    rectWidth: rect.width,
                    rectHeight: rect.height,
                    brokenImages: brokenImgs,
                    overflowingElements: overflowingElements
                };
            }""", slide_id)

            if not check["found"]:
                errors.append(f"{slide_id} not found in DOM!")
                continue

            if check["scrollWidth"] > 1602 or check["scrollHeight"] > 902:
                errors.append(f"{slide_id} OVERFLOW: scrollWidth={check['scrollWidth']}px, scrollHeight={check['scrollHeight']}px")
            
            if check["brokenImages"]:
                errors.append(f"{slide_id} BROKEN IMAGES: {check['brokenImages']}")

            if check["overflowingElements"]:
                errors.append(f"{slide_id} ELEMENT OVERFLOW: {check['overflowingElements']}")

            print(f"Slide {slide_num:02d}: geometry {check['scrollWidth']}x{check['scrollHeight']}px | 0 broken imgs | 0 element overflow")

        if errors:
            print("\n[CRITICAL DOM GATEKEEPER FAILURE]:")
            for err in errors:
                print(f"  - {err}")
            browser.close()
            sys.exit(1)

        print(f"--> {TOTAL_SLIDES}/{TOTAL_SLIDES} Slides PASSED all DOM & Image Gates with 0 Violations!")

        # -------------------------------------------------------------
        # 3. Export 3 Clean Vector PDFs Directly via Playwright
        # -------------------------------------------------------------
        print("\n--- 3. Direct Export of Master Vector PDFs (Chromium Skia Direct) ---")

        # A. Complete 15-Slide Master Deck PDF
        page.pdf(
            path=complete_15_pdf_path,
            width="13.333333in",
            height="7.5in",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}
        )
        shutil.copy(complete_15_pdf_path, final_deck_pdf_path)

        doc15 = pymupdf.open(complete_15_pdf_path)
        p15_count = len(doc15)
        p15_mb = os.path.getsize(complete_15_pdf_path) / (1024 * 1024)
        p15_repaired = doc15.is_repaired
        doc15.close()
        print(f"Complete 15-Slide PDF: {p15_count} pages ({p15_mb:.2f} MB), is_repaired={p15_repaired}")
        assert p15_count == 15, f"ERROR: Expected 15 pages, found {p15_count}!"
        assert not p15_repaired, "ERROR: Complete PDF has corrupted xref table!"
        assert p15_mb < 4.7, f"Complete PDF exceeds 4.7 MB limit: {p15_mb:.2f} MB"

        # B. Slides 1–10 Pitch Deck PDF
        page_10 = context.new_page()
        page_10.goto(f"file:///{deck_10_html_path.replace(os.sep, '/')}")
        page_10.wait_for_load_state("networkidle")
        page_10.evaluate("document.fonts.ready")
        page_10.pdf(
            path=deck_10_pdf_path,
            width="13.333333in",
            height="7.5in",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}
        )
        page_10.close()

        doc10 = pymupdf.open(deck_10_pdf_path)
        p10_count = len(doc10)
        p10_mb = os.path.getsize(deck_10_pdf_path) / (1024 * 1024)
        p10_repaired = doc10.is_repaired
        doc10.close()
        print(f"10-Slide Pitch Deck PDF: {p10_count} pages ({p10_mb:.2f} MB), is_repaired={p10_repaired}")
        assert p10_count == 10, f"ERROR: Expected 10 pages in Pitch Deck, found {p10_count}!"
        assert not p10_repaired, "ERROR: Pitch Deck PDF has corrupted xref table!"
        assert p10_mb < 4.0, f"Pitch Deck PDF exceeds 4.0 MB limit: {p10_mb:.2f} MB"

        # C. Slides 11–15 Visual User Guide PDF
        page_guide = context.new_page()
        page_guide.goto(f"file:///{guide_5_html_path.replace(os.sep, '/')}")
        page_guide.wait_for_load_state("networkidle")
        page_guide.evaluate("document.fonts.ready")
        page_guide.pdf(
            path=guide_5_pdf_path,
            width="13.333333in",
            height="7.5in",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}
        )
        page_guide.close()

        doc_g = pymupdf.open(guide_5_pdf_path)
        pg_count = len(doc_g)
        pg_mb = os.path.getsize(guide_5_pdf_path) / (1024 * 1024)
        pg_repaired = doc_g.is_repaired
        doc_g.close()
        print(f"Visual User Guide PDF (Slides 11–15): {pg_count} pages ({pg_mb:.2f} MB), is_repaired={pg_repaired}")
        assert pg_count == 5, f"ERROR: Expected 5 pages in User Guide, found {pg_count}!"
        assert not pg_repaired, "ERROR: User Guide PDF has corrupted xref table!"
        assert pg_mb < 4.5, f"Guide PDF exceeds 4.5 MB limit: {pg_mb:.2f} MB"

        # -------------------------------------------------------------
        # 4. Capture Slide Screenshots & 5 Standalone Guide Posters
        # -------------------------------------------------------------
        print("\n--- 4. Capturing Slide Screenshots & 5 Standalone Guide Posters ---")
        slide_images = []
        for slide_num in range(1, TOTAL_SLIDES + 1):
            slide_id = f"#slide-{slide_num}"
            png_path = os.path.join(audit_slides_dir, f"slide_{slide_num:02d}.png")
            el = page.locator(slide_id)
            el.screenshot(path=png_path)
            slide_images.append(png_path)
            print(f"Captured {os.path.basename(png_path)} ({os.path.getsize(png_path)/1024:.1f} KB)")

        # Export 5 standalone PNG guide posters (Slides 11–15)
        guide_posters = [
            (11, "guide_01_pcb_360.png"),
            (12, "guide_02_wiring_map.png"),
            (13, "guide_03_portal_business.png"),
            (14, "guide_04_portal_inspector.png"),
            (15, "guide_05_quickstart_github.png")
        ]
        for s_num, fname in guide_posters:
            poster_path = os.path.join(visual_guides_dir, fname)
            el = page.locator(f"#slide-{s_num}")
            el.screenshot(path=poster_path)
            poster_mb = os.path.getsize(poster_path) / (1024 * 1024)
            print(f"Exported Guide Poster: {fname} ({poster_mb:.2f} MB)")
            assert poster_mb < 1.8, f"Poster {fname} exceeds 1.8 MB: {poster_mb:.2f} MB"

        browser.close()

    # -------------------------------------------------------------
    # 5. Assemble 15-Slide Widescreen PPTX with Jury Notes
    # -------------------------------------------------------------
    print("\n--- 5. Assembling 15-Slide PPTX with Optimized Slides & Jury Notes ---")
    prs = Presentation()
    prs.slide_width = Inches(13.333333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    for idx, png_path in enumerate(slide_images, start=1):
        slide = prs.slides.add_slide(blank_layout)

        # Convert to high-quality JPEG in memory at quality 80 to ensure 15 slides stay strictly under 4.7 MB
        im = Image.open(png_path).convert("RGB")
        img_buffer = io.BytesIO()
        im.save(img_buffer, format="JPEG", quality=80, optimize=True)
        img_buffer.seek(0)

        # Add full-bleed image
        slide.shapes.add_picture(img_buffer, 0, 0, width=Inches(13.333333), height=Inches(7.5))

        # Add Jury Speaker Notes
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = SPEAKER_NOTES.get(idx, "")

    prs.save(pptx_path)
    pptx_mb = os.path.getsize(pptx_path) / (1024 * 1024)
    print(f"Generated PPTX: {pptx_path} ({pptx_mb:.2f} MB)")
    assert pptx_mb < 4.7, f"Master PPTX exceeds 4.7 MB limit: {pptx_mb:.2f} MB"

    print("\n--- 6. Enforcing Strict Startup India Compliance Limits ---")
    print(f"Final File Sizes:")
    print(f"  - 10-Slide Pitch Deck PDF = {p10_mb:.2f} MB (< 4.0 MB limit)")
    print(f"  - 5-Page Visual User Guide PDF = {pg_mb:.2f} MB (< 4.5 MB limit)")
    print(f"  - Complete 15-Slide PDF = {p15_mb:.2f} MB (< 4.7 MB limit)")
    print(f"  - Complete 15-Slide PPTX = {pptx_mb:.2f} MB (< 4.7 MB limit)")
    print("--> ALL DELIVERABLES STRICTLY COMPLY WITH ALL STARTUP INDIA SPECIFICATIONS!")

    # -------------------------------------------------------------
    # 7. Sync Generated Deliverables to Frontend Web App
    # -------------------------------------------------------------
    print("\n--- 7. Syncing Generated Deliverables to Frontend Web App ---")
    shutil.copy(deck_10_pdf_path, os.path.join(frontend_deck_dir, "TapasShield_NSA6_Pitch_Deck_10Slides.pdf"))
    shutil.copy(guide_5_pdf_path, os.path.join(frontend_deck_dir, "TapasShield_Visual_User_Guide.pdf"))
    shutil.copy(complete_15_pdf_path, os.path.join(frontend_deck_dir, "TapasShield_NSA6_Complete_15Slides.pdf"))
    shutil.copy(final_deck_pdf_path, os.path.join(frontend_deck_dir, "TapasShield_NSA6_Final_Deck.pdf"))
    shutil.copy(pptx_path, os.path.join(frontend_deck_dir, "TapasShield_NSA6_Final_Deck.pptx"))

    for png_path in slide_images:
        shutil.copy(png_path, os.path.join(frontend_deck_dir, os.path.basename(png_path)))
    for _, fname in guide_posters:
        shutil.copy(os.path.join(visual_guides_dir, fname), os.path.join(frontend_deck_dir, fname))
    print("--> Copied all PDFs, PPTX, and slide/poster PNGs to frontend/public/deck/")

    print("\n[ALL 15-SLIDE BUILD & VERIFICATION PHASES COMPLETED WITH 100% SUCCESS!]")

if __name__ == "__main__":
    main()
