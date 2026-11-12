"""Builds Lab7_Report.pdf from the four screenshots in the screenshots/ folder.
Usage:  pip install pillow   then   python make_pdf.py
"""
from PIL import Image, ImageDraw, ImageFont
import os, sys, glob

NAME, SRN = "Sai Likhith S", "PES1UG24AM239"
STEPS = [
    ("step2_buggy_run.png",    "Step 2: Buggy processor.py - python processor.py"),
    ("step4_tests_failing.png", "Step 4: pytest test_processor.py against the buggy processor.py (tests failing)"),
    ("step5_fixed_run.png",    "Step 5: Fixed processor.py - python processor.py"),
    ("step6_tests_passing.png", "Step 6: pytest test_processor.py against the fixed processor.py (tests passing)"),
]
W = 1600
font = big = None
for name in ("arial.ttf", "DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
    try:
        font = ImageFont.truetype(name, 30); big = ImageFont.truetype(name, 48)
        break
    except OSError:
        continue
if font is None:
    font = big = ImageFont.load_default()

pages = []
cover = Image.new("RGB", (W, 900), "white"); d = ImageDraw.Draw(cover)
d.text((60, 120), "Lab 7: Fuzzing for Input Validation Bugs", fill="black", font=big)
d.text((60, 260), f"Name: {NAME}", fill="black", font=font)
d.text((60, 320), f"SRN: {SRN}", fill="black", font=font)
pages.append(cover)

for fname, caption in STEPS:
    # a step may have extra continuation screenshots: step4_tests_failing_2.png, ...
    base, ext = os.path.splitext(fname)
    files = [os.path.join("screenshots", fname)]
    files += sorted(glob.glob(os.path.join("screenshots", base + "_*" + ext)))
    if not os.path.exists(files[0]):
        sys.exit(f"Missing screenshot: {files[0]}")
    for i, path in enumerate(files):
        img = Image.open(path).convert("RGB")
        img = img.resize((W - 120, int(img.height * (W - 120) / img.width)))
        page = Image.new("RGB", (W, img.height + 160), "white")
        label = caption if i == 0 else caption + f" (continued, part {i + 1})"
        ImageDraw.Draw(page).text((60, 50), label, fill="black", font=font)
        page.paste(img, (60, 110))
        pages.append(page)

pages[0].save("Lab7_Report.pdf", save_all=True, append_images=pages[1:])
print("Created Lab7_Report.pdf")
