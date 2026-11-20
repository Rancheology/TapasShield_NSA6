import os
import shutil
from PIL import Image

src_dir = os.path.join("presentation", "visual_guide_assets")
dst_dir = os.path.join("presentation", "deck_html", "visual_assets")
os.makedirs(dst_dir, exist_ok=True)

# 1. Process portal_full_business
im_biz = Image.open(os.path.join(src_dir, "portal_full_business.png")).convert("RGB")
# Scale down to 1440 width for sharp vector-like display and optimal PDF size
scale_biz = 1440 / im_biz.width
im_biz = im_biz.resize((1440, int(im_biz.height * scale_biz)), Image.Resampling.LANCZOS)
biz_dst = os.path.join(dst_dir, "portal_full_business.jpg")
im_biz.save(biz_dst, format="JPEG", quality=88, optimize=True)
print(f"Saved {biz_dst}: size={im_biz.size}, {os.path.getsize(biz_dst)/1024:.1f} KB")

# 2. Process portal_full_inspector
im_insp = Image.open(os.path.join(src_dir, "portal_full_inspector.png")).convert("RGB")
scale_insp = 1440 / im_insp.width
im_insp = im_insp.resize((1440, int(im_insp.height * scale_insp)), Image.Resampling.LANCZOS)
insp_dst = os.path.join(dst_dir, "portal_full_inspector.jpg")
im_insp.save(insp_dst, format="JPEG", quality=88, optimize=True)
print(f"Saved {insp_dst}: size={im_insp.size}, {os.path.getsize(insp_dst)/1024:.1f} KB")

# 3. Process portal_zoom_controls
im_ctrl = Image.open(os.path.join(src_dir, "portal_zoom_controls.png")).convert("RGB")
scale_ctrl = 1440 / im_ctrl.width
im_ctrl = im_ctrl.resize((1440, int(im_ctrl.height * scale_ctrl)), Image.Resampling.LANCZOS)
ctrl_dst = os.path.join(dst_dir, "portal_zoom_controls.jpg")
im_ctrl.save(ctrl_dst, format="JPEG", quality=88, optimize=True)
print(f"Saved {ctrl_dst}: size={im_ctrl.size}, {os.path.getsize(ctrl_dst)/1024:.1f} KB")

# 4. Process portal_zoom_audit_cert
im_cert = Image.open(os.path.join(src_dir, "portal_zoom_audit_cert.png")).convert("RGB")
scale_cert = 1440 / im_cert.width
im_cert = im_cert.resize((1440, int(im_cert.height * scale_cert)), Image.Resampling.LANCZOS)
cert_dst = os.path.join(dst_dir, "portal_zoom_audit_cert.jpg")
im_cert.save(cert_dst, format="JPEG", quality=88, optimize=True)
print(f"Saved {cert_dst}: size={im_cert.size}, {os.path.getsize(cert_dst)/1024:.1f} KB")

# 5. Process qr-code_github.png
im_qr = Image.open(os.path.join(src_dir, "qr-code_github.png")).convert("RGB")
im_qr = im_qr.resize((400, 400), Image.Resampling.LANCZOS)
qr_dst = os.path.join(dst_dir, "qr-code_github.png")
im_qr.save(qr_dst, format="PNG", optimize=True)
print(f"Saved {qr_dst}: size={im_qr.size}, {os.path.getsize(qr_dst)/1024:.1f} KB")

print("\nAll new visual guide assets prepared cleanly!")

