import os
import pymupdf
from pptx import Presentation

FINAL_DECK_PDF = os.path.join("presentation", "TapasShield_NSA6_Final_Deck.pdf")
FINAL_DECK_PPTX = os.path.join("presentation", "TapasShield_NSA6_Final_Deck.pptx")
USER_GUIDE_PDF = os.path.join("presentation", "TapasShield_Visual_User_Guide.pdf")
VISUAL_GUIDES_DIR = os.path.join("presentation", "visual_guides")
PUBLIC_DECK_DIR = os.path.join("frontend", "public", "deck")

def test_final_master_pdf():
    """Verify 14-slide master PDF integrity, page count, and strict size limit (< 4.7 MB)."""
    assert os.path.exists(FINAL_DECK_PDF), f"Missing {FINAL_DECK_PDF}"
    doc = pymupdf.open(FINAL_DECK_PDF)
    assert len(doc) == 14, f"Expected 14 pages in master PDF, got {len(doc)}"
    doc.close()
    
    size_mb = os.path.getsize(FINAL_DECK_PDF) / (1024 * 1024)
    assert size_mb < 4.7, f"Master PDF size {size_mb:.2f} MB exceeds 4.7 MB limit"
    assert size_mb > 1.0, f"Master PDF suspiciously small: {size_mb:.2f} MB"

def test_final_master_pptx():
    """Verify 14-slide master PPTX integrity, slide count, aspect ratio, speaker notes, and size limit (< 4.7 MB)."""
    assert os.path.exists(FINAL_DECK_PPTX), f"Missing {FINAL_DECK_PPTX}"
    prs = Presentation(FINAL_DECK_PPTX)
    assert len(prs.slides) == 14, f"Expected 14 slides in master PPTX, got {len(prs.slides)}"
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
    """Verify standalone 4-page visual user guide PDF exists and is < 2.8 MB."""
    assert os.path.exists(USER_GUIDE_PDF), f"Missing {USER_GUIDE_PDF}"
    doc = pymupdf.open(USER_GUIDE_PDF)
    assert len(doc) == 4, f"Expected 4 pages in user guide PDF, got {len(doc)}"
    doc.close()
    
    size_mb = os.path.getsize(USER_GUIDE_PDF) / (1024 * 1024)
    assert size_mb < 2.8, f"User Guide PDF size {size_mb:.2f} MB exceeds 2.8 MB limit"
    assert size_mb > 0.3, f"User Guide PDF suspiciously small: {size_mb:.2f} MB"

def test_standalone_png_guide_posters():
    """Verify all 4 standalone PNG guide posters exist, are synced to public deck, and are < 1.8 MB each."""
    posters = [
        "guide_01_pcb_360.png",
        "guide_02_wiring_map.png",
        "guide_03_portal_mechanics.png",
        "guide_04_quickstart_storyboard.png"
    ]
    for p_name in posters:
        p_src = os.path.join(VISUAL_GUIDES_DIR, p_name)
        p_dest = os.path.join(PUBLIC_DECK_DIR, p_name)
        assert os.path.exists(p_src), f"Missing guide poster: {p_src}"
        assert os.path.exists(p_dest), f"Missing synced public poster: {p_dest}"
        
        sz_mb = os.path.getsize(p_src) / (1024 * 1024)
        assert sz_mb < 1.8, f"Poster {p_name} ({sz_mb:.2f} MB) exceeds 1.8 MB"
        assert sz_mb > 0.1, f"Poster {p_name} suspiciously small: {sz_mb:.2f} MB"

