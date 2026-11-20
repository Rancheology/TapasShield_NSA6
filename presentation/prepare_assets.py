import os
from PIL import Image

deck_html_dir = os.path.join("presentation", "deck_html")

rgb_targets = [
    ("assets/live_dual_register.png", "assets/live_dual_register.jpg", 1440, 88),
    ("assets/live_govt_tamper_audit.png", "assets/live_govt_tamper_audit.jpg", 1440, 88),
    ("assets/live_scale_predictive.png", "assets/live_scale_predictive.jpg", 1440, 88),
    ("visual_assets/physical_wiring_hero.png", "visual_assets/physical_wiring_hero.jpg", 1440, 88),
    ("visual_assets/ui_crop_step1_scenarios.png", "visual_assets/ui_crop_step1_scenarios.jpg", 1440, 88),
    ("visual_assets/ui_crop_step2_scale_roi.png", "visual_assets/ui_crop_step2_scale_roi.jpg", 1440, 88),
    ("visual_assets/ui_crop_step3_tamper_cert.png", "visual_assets/ui_crop_step3_tamper_cert.jpg", 1440, 88),
    ("visual_assets/ui_full_business.png", "visual_assets/ui_full_business.jpg", 1440, 88),
    ("visual_assets/ui_full_inspector.png", "visual_assets/ui_full_inspector.jpg", 1440, 88),
]

for src_rel, dst_rel, max_dim, q in rgb_targets:
    src_path = os.path.join(deck_html_dir, src_rel)
    dst_path = os.path.join(deck_html_dir, dst_rel)
    if os.path.exists(src_path):
        im = Image.open(src_path).convert("RGB")
        if max(im.size) > max_dim:
            scale = max_dim / max(im.size)
            new_size = (int(im.size[0] * scale), int(im.size[1] * scale))
            im = im.resize(new_size, Image.Resampling.LANCZOS)
        im.save(dst_path, format="JPEG", quality=q, optimize=True)
        print(f"Generated {dst_rel}: size={im.size}, file_size={os.path.getsize(dst_path)/1024:.1f} KB")
    else:
        print(f"WARNING: {src_path} not found!")

print("All raster RGB assets prepared cleanly.")
