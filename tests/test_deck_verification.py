import os
import pytest
from pptx import Presentation
from pptx.util import Inches
from pptx.enum.shapes import MSO_SHAPE_TYPE

from presentation.generate_nsa6_deck import verify_pptx_integrity

PPTX_PATH = os.path.join("presentation", "TapasShield_NSA6_Pitch_Deck.pptx")
ASSETS_DIR = os.path.join("presentation", "assets")
PUBLIC_DECK_DIR = os.path.join("frontend", "public", "deck")

def test_deck_file_exists():
    """Verify official PPTX presentation file exists and is substantial."""
    assert os.path.exists(PPTX_PATH), f"Missing {PPTX_PATH}"
    size = os.path.getsize(PPTX_PATH)
    assert size > 500_000, f"PPTX file unexpectedly small: {size} bytes"

def test_deck_chart_assets():
    """Verify all 5 300-DPI charts exist in presentation/assets and frontend/public/deck."""
    expected_charts = [
        "chart_thermodynamic_drift.png",
        "diagram_crypto_pipeline.png",
        "chart_afe_loop_calibration.png",
        "chart_bom_and_roi.png",
        "portal_dual_register_ui.png"
    ]
    for ch in expected_charts:
        src_p = os.path.join(ASSETS_DIR, ch)
        dest_p = os.path.join(PUBLIC_DECK_DIR, ch)
        assert os.path.exists(src_p), f"Missing source chart: {src_p}"
        assert os.path.exists(dest_p), f"Missing synced public chart: {dest_p}"
        assert os.path.getsize(src_p) > 50_000, f"Chart {src_p} suspiciously small"

def test_deck_integrity_audit():
    """Formally run verify_pptx_integrity ensuring 10 slides, zero overflows, >=6 pictures."""
    assert verify_pptx_integrity(PPTX_PATH) is True

def test_deck_slide_details():
    """Verify slide count, aspect ratio, and layout properties."""
    prs = Presentation(PPTX_PATH)
    assert len(prs.slides) == 10
    
    # 16:9 Widescreen dimensions
    assert abs(prs.slide_width.inches - 13.333) < 0.01
    assert abs(prs.slide_height.inches - 7.5) < 0.01

    for i, slide in enumerate(prs.slides):
        # Every slide has background, kicker, title, rubric, footer line, footer left, footer right, etc.
        assert len(slide.shapes) >= 6, f"Slide {i+1} has fewer than 6 shapes: {len(slide.shapes)}"

