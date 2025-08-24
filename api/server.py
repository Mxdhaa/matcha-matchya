from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import pytesseract
from PIL import Image
import io
import re

app = Flask(__name__)
CORS(app)

# ---------------- Known Skills ----------------
KNOWN_SKILLS = {
  "python", "java", "c", "c++", "c#", "go", "rust", "ruby", "php", "swift", "kotlin",
  "javascript", "typescript", "dart", "r", "scala", "matlab",

  "html", "css", "sass", "tailwind", "bootstrap",
  "react", "next.js", "angular", "vue", "svelte",
  "node.js", "express", "fastify", "nestjs",

  "sql", "mysql", "postgresql", "sqlite", "oracle", "mssql",
  "mongodb", "dynamodb", "cassandra", "redis", "elasticsearch",

  "git", "github", "gitlab", "bitbucket",
  "docker", "kubernetes", "terraform", "ansible", "jenkins", "circleci", "travis", "github actions",

  "aws", "azure", "gcp", "firebase", "heroku", "netlify", "vercel",

  "flask", "django", "fastapi", "spring", "hibernate",
  "rails", "laravel", "symfony", "express",

  "tensorflow", "pytorch", "scikit-learn", "keras",
  "xgboost", "lightgbm", "catboost",
  "huggingface", "transformers", "spacy", "nltk",
  "opencv", "mediapipe",

  "nlp", "llm", "gpt", "bert", "gcn", "gnn",

  "pandas", "numpy", "scipy", "matplotlib", "seaborn", "plotly", "d3.js",

  "ci", "cd", "cicd", "automation", "testing", "pytest", "unittest",
  "playwright", "selenium", "cypress",

  "linux", "bash", "shell", "powershell", "windows", "unix"
}

# ---------- Helpers ----------

def extract_text_from_pdf(file_bytes):
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_image(file_bytes):
    img = Image.open(io.BytesIO(file_bytes))
    return pytesseract.image_to_string(img)

def clean_tokens(text):
    words = re.findall(r"[a-zA-Z0-9\+\#\.]+", text.lower())
    return set(w.strip(".") for w in words if len(w) > 1)

# ---------- API Endpoint ----------

@app.route("/api/analyze-resume", methods=["POST"])
def analyze():
    file = request.files.get("file")
    job_desc = request.form.get("jobDescription", "")

    if not file or not job_desc:
        return jsonify({"error": "Missing file or job description"}), 400

    # Step 1: Extract text
    if file.filename.lower().endswith(".pdf"):
        resume_text = extract_text_from_pdf(file.read())
    else:
        resume_text = extract_text_from_image(file.read())

    # Step 2: Tokenize + filter by known skills
    resume_words = clean_tokens(resume_text) & KNOWN_SKILLS
    jd_words = clean_tokens(job_desc) & KNOWN_SKILLS

    # Step 3: Compare
    matched = sorted(resume_words & jd_words)
    missing = sorted(jd_words - resume_words)
    extra = sorted(resume_words - jd_words)

    similarity = round((len(matched) / len(jd_words) * 100), 1) if jd_words else 0

    improvements = []
    if missing:
        improvements.append("Add missing skills: " + ", ".join(missing[:10]))
    if not improvements:
        improvements.append("Resume already covers most job requirements!")

    return jsonify({
        "similarity": similarity,
        "matchedSkills": matched,
        "missingSkills": missing,
        "extraSkills": extra,
        "improvements": improvements
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
