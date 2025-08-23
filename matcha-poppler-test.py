from pdf2image import convert_from_path
from pathlib import Path

pdf = r"C:\Users\Admin\Documents\matcha-matchya\sample.pdf"   # change me
out_dir = Path(r"C:\Users\Admin\Documents\matcha-matchya\out")
out_dir.mkdir(parents=True, exist_ok=True)

images = convert_from_path(
    pdf, 
    dpi=200, 
    fmt="png",
    poppler_path=r"C:\Release-25.07.0-0\poppler-25.07.0\Library\bin"
)

for i, img in enumerate(images, 1):
    img.save(out_dir / f"page_{i}.png")
print(f"Saved {len(images)} pages to {out_dir}")
