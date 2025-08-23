from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from .ocr import pdf_or_image_bytes_to_text
from .nlp import extract_skills
from .scoring import coverage_score, fuzzy_overlap_score, keyword_hit_rate, overall
from .suggestions import generate_suggestions
from .llm import gemini_suggestions
from .models import MatchRequest, MatchResponse, UploadResponse

app = FastAPI(title="Matcha‑Matchya API", version="0.1.0")


@app.post("/upload", response_model=UploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    blob = await file.read()
    resume_text, meta = pdf_or_image_bytes_to_text(blob, file.filename)
    return {"resume_text": resume_text, "meta": meta}


@app.post("/match", response_model=MatchResponse)
async def match_resume(
    file: UploadFile = File(...),
    jd_text: str = Form(...),
):
    blob = await file.read()
    resume_text, _ = pdf_or_image_bytes_to_text(blob, file.filename)

    rskills = extract_skills(resume_text)
    jskills = extract_skills(jd_text)

    s_cov = coverage_score(rskills, jskills)
    s_fuz = fuzzy_overlap_score(resume_text, jd_text)
    s_khr = keyword_hit_rate(resume_text, jd_text, jskills)
    scores = {"coverage": s_cov, "fuzzy": s_fuz, "khr": s_khr}

    matched = sorted(set(rskills) & set(jskills))
    missing = sorted(set(jskills) - set(rskills))

    sug = generate_suggestions(missing)
    llm = gemini_suggestions(resume_text, jd_text, missing)

    return MatchResponse(
        score_overall=overall(scores),
        scores=scores,
        extracted_skills=rskills,
        jd_skills=jskills,
        matched_skills=matched,
        missing_skills=missing,
        suggestions=sug,
        llm_suggestions=llm,
    )


@app.get("/", response_class=HTMLResponse)
async def root_page():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())
