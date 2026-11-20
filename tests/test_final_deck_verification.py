import os
import pymupdf
from pptx import Presentation

FINAL_DECK_PDF = os.path.join("presentation", "TapasShield_NSA6_Final_Deck.pdf")
FINAL_DECK_PPTX = os.path.join("presentation", "TapasShield_NSA6_Final_Deck.pptx")
COMPLETE_15_PDF = os.path.join("presentation", "TapasShield_NSA6_Complete_15Slides.pdf")
PITCH_DECK_10_PDF = os.path.join("presentation", "TapasShield_NSA6_Pitch_Deck_10Slides.pdf")
USER_GUIDE_PDF = os.path.join("presentation", "TapasShield_Visual_User_Guide.pdf")
VISUAL_GUIDES_DIR = os.path.join("presentation", "visual_guides")
PUBLIC_DECK_DIR = os.path.join("frontend", "public", "deck")

def test_final_master_pdf():
    """Verify 15-slide master PDF integrity, page count, and strict size limit (< 4.7 MB)."""
    assert os.path.exists(FINAL_DECK_PDF), f"Missing {FINAL_DECK_PDF}"
    doc = pymupdf.open(FINAL_DECK_PDF)
    assert len(doc) == 15, f"Expected 15 pages in master PDF, got {len(doc)}"
    assert not doc.is_repaired, "Master PDF has corrupted xref table!"
    doc.close()
    
    size_mb = os.path.getsize(FINAL_DECK_PDF) / (1024 * 1024)
    assert size_mb < 4.7, f"Master PDF size {size_mb:.2f} MB exceeds 4.7 MB limit"
    assert size_mb > 1.0, f"Master PDF suspiciously small: {size_mb:.2f} MB"

def test_10slide_pitch_deck_and_complete_15slide_pdf():
    """Verify standalone 10-slide Pitch Deck (< 4.0 MB) and Complete 15-Slide PDF (< 4.7 MB)."""
    assert os.path.exists(PITCH_DECK_10_PDF), f"Missing {PITCH_DECK_10_PDF}"
    doc10 = pymupdf.open(PITCH_DECK_10_PDF)
    assert len(doc10) == 10, f"Expected 10 pages in Pitch Deck, got {len(doc10)}"
    assert not doc10.is_repaired
    doc10.close()
    size10_mb = os.path.getsize(PITCH_DECK_10_PDF) / (1024 * 1024)
    assert size10_mb < 4.0, f"Pitch Deck PDF {size10_mb:.2f} MB exceeds 4.0 MB limit"

    assert os.path.exists(COMPLETE_15_PDF), f"Missing {COMPLETE_15_PDF}"
    doc15 = pymupdf.open(COMPLETE_15_PDF)
    assert len(doc15) == 15, f"Expected 15 pages in Complete PDF, got {len(doc15)}"
    assert not doc15.is_repaired
    doc15.close()
    size15_mb = os.path.getsize(COMPLETE_15_PDF) / (1024 * 1024)
    assert size15_mb < 4.7, f"Complete PDF {size15_mb:.2f} MB exceeds 4.7 MB limit"

def test_final_master_pptx():
    """Verify 15-slide master PPTX integrity, slide count, aspect ratio, speaker notes, and size limit (< 4.7 MB)."""
    assert os.path.exists(FINAL_DECK_PPTX), f"Missing {FINAL_DECK_PPTX}"
    prs = Presentation(FINAL_DECK_PPTX)
    assert len(prs.slides) == 15, f"Expected 15 slides in master PPTX, got {len(prs.slides)}"
    assert abs(prs.slide_width.inches - 13.333333) < 0.01
    assert abs(prs.slide_height.inches - 7.5) < 0.01

    # Verify speaker notes are populated for every slide
    for i, slide in enumerate(prs.slides, start=1):
        notes_text = slide.notes_slide.notes_text_frame.text
        assert len(notes_text) > 50, f"Slide {i} speaker notes missing or too short: {len(notes_text)} chars"

    size_mb = os.path.getsize(FINAL_DECK_PPTX) / (1024 * 1024)
    assert size_mb < 4.7, f"Master PPTX size {size_mb:.2f} MB exceeds 4.7 MB limit"
    assert size_mb > 1.0, f"Master PPTX suspiciously small: {size_mb:.2f} MB"

def test_standalone_user_guide_pdf():
    """Verify standalone 5-page visual user guide PDF exists, is < 4.5 MB, and has valid xref."""
    assert os.path.exists(USER_GUIDE_PDF), f"Missing {USER_GUIDE_PDF}"
    doc = pymupdf.open(USER_GUIDE_PDF)
    assert len(doc) == 5, f"Expected 5 pages in user guide PDF, got {len(doc)}"
    assert not doc.is_repaired, "User Guide PDF has corrupted xref table!"
    doc.close()
    
    size_mb = os.path.getsize(USER_GUIDE_PDF) / (1024 * 1024)
    assert size_mb < 4.5, f"User Guide PDF size {size_mb:.2f} MB exceeds 4.5 MB limit"
    assert size_mb > 0.3, f"User Guide PDF suspiciously small: {size_mb:.2f} MB"

def test_standalone_png_guide_posters():
    """Verify all 5 standalone PNG guide posters exist, are synced to public deck, and are < 1.8 MB each."""
    posters = [
        "guide_01_pcb_360.png",
        "guide_02_wiring_map.png",
        "guide_03_portal_business.png",
        "guide_04_portal_inspector.png",
        "guide_05_quickstart_github.png"
    ]
    for p_name in posters:
        p_src = os.path.join(VISUAL_GUIDES_DIR, p_name)
        p_dest = os.path.join(PUBLIC_DECK_DIR, p_name)
        assert os.path.exists(p_src), f"Missing source poster: {p_src}"
        assert os.path.exists(p_dest), f"Missing public synced poster: {p_dest}"
        p_mb = os.path.getsize(p_src) / (1024 * 1024)
        assert p_mb < 1.8, f"Poster {p_name} ({p_mb:.2f} MB) exceeds 1.8 MB"
