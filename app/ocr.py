from typing import Tuple, Dict
import tempfile
import pytesseract
from pdf2image import convert_from_bytes


# If tesseract is not on PATH on Windows, set it here, e.g.:
# pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"




def pdf_or_image_bytes_to_text(file_bytes: bytes, filename: str) -> Tuple[str, Dict[str, str]]:
name = filename.lower()
meta = {"filename": filename}


if name.endswith(".pdf"):
images = convert_from_bytes(file_bytes, dpi=300, fmt="png")
text_parts = []
for img in images:
text_parts.append(pytesseract.image_to_string(img))
return "\n".join(text_parts), meta


# Assume image otherwise
with tempfile.NamedTemporaryFile(suffix=name) as tmp:
tmp.write(file_bytes)
tmp.flush()
text = pytesseract.image_to_string(tmp.name)
return text, meta