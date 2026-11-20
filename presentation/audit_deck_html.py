import re
import os
from PIL import Image

html_path = "presentation/deck_html/index.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
print(f"Total img tags in index.html: {len(imgs)}")
all_exist = True
for img in imgs:
    path = os.path.join("presentation/deck_html", img)
    if not os.path.exists(path):
        print(f"  MISSING: {img} -> {path}")
        all_exist = False
    else:
        im = Image.open(path)
        sz_kb = os.path.getsize(path) / 1024
        print(f"  OK: {img} ({im.size[0]}x{im.size[1]}, {sz_kb:.1f} KB)")

if all_exist:
    print("ALL IMAGES PRESENT AND VALID!")
else:
    print("SOME IMAGES MISSING!")

# Check all 15 slide IDs
for i in range(1, 16):
    sid = f'id="slide-{i}"'
    if sid in html:
        print(f"Slide {i:02d}: FOUND")
    else:
        print(f"Slide {i:02d}: MISSING!")
