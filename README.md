# Matcha‑Matchya (MVP)


## 1) Prereqs
- Poppler installed and on PATH (`pdftoppm` available).
- Tesseract‑OCR installed and on PATH. If on Windows, set `pytesseract.pytesseract.tesseract_cmd` in `app/ocr.py`.


## 2) Setup
```bash
python -m venv .venv && . .venv/Scripts/activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
# spaCy model (optional)
python -m spacy download en_core_web_sm || echo "Proceeding without model"