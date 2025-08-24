# api/analyze-resume.py
from http.server import BaseHTTPRequestHandler
import json
import re

try:
    from app import nlp, scoring  # your files: app/nlp.py, app/scoring.py
except Exception:
    nlp = scoring = None


def _norm(s: str):
    return re.sub(r"[^a-z0-9+.#\- ]+", " ", s.lower()).split()


def _analyze_with_locals(resume_text: str, jd_text: str):
    """
    If your app/nlp.py and app/scoring.py expose helpers, you can wire them here.
    Fallback to a safe mock otherwise.
    """
    SKILLS = [
        'python','pytorch','tensorflow','scikit-learn','docker','kubernetes',
        'react','node.js','typescript','javascript','sql','mongodb','postgresql',
        'ci/cd','github actions','aws','gcp','azure','nlp','opencv','tesseract'
    ]

    in_resume = [s for s in SKILLS if s in resume_text.lower()]
    in_jd     = [s for s in SKILLS if s in jd_text.lower()]

    matched = sorted(set(x for x in in_resume if x in in_jd))
    missing = sorted(set(x for x in in_jd if x not in in_resume))
    extra   = sorted(set(x for x in in_resume if x not in in_jd))

    r_tok = set(_norm(resume_text))
    j_tok = set(_norm(jd_text))
    overlap = len(r_tok & j_tok)
    denom = max(10, len(j_tok) or 0)
    similarity = max(0, min(100, round(overlap / denom * 100)))

    improvements = []
    if missing:
        improvements.append(f"Add experience with: {', '.join(missing)}")
    if not resume_text.strip():
        improvements.append("Could not read resume text (PDF/OCR not implemented).")
    if not jd_text.strip():
        improvements.append("Paste a job description for better matching.")
    if not improvements:
        improvements = ["Looks good. Consider adding measurable, impact‑focused bullets."]

    return {
        "similarity": similarity,
        "matchedSkills": matched,
        "missingSkills": missing,
        "extraSkills": extra,
        "improvements": improvements
    }


class handler(BaseHTTPRequestHandler):
    def _send(self, code=200, payload=None):
        body = json.dumps(payload or {}).encode()
        self.send_response(code)
        # CORS for local testing & browser fetch
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send(200, {})

    def do_POST(self):
        try:
            length = int(self.headers.get("content-length", "0"))
            raw = self.rfile.read(length) if length > 0 else b"{}"
            data = json.loads(raw.decode("utf-8") or "{}")
            resume_text = data.get("resumeText", "") or ""
            jd_text     = data.get("jobDescription", "") or ""

            # If you later wire real analyzers:
            # if nlp and scoring:
            #     ... call into your modules ...
            result = _analyze_with_locals(resume_text, jd_text)

            self._send(200, result)
        except Exception as e:
            self._send(500, {"error": f"Server error: {e!s}"})


# Vercel discovers the `handler` class automatically for Python functions.
