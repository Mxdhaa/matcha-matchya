# app/matcher.py
import re, string
import fitz  # PyMuPDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import process, fuzz

SKILL_DB = [
    "python","java","c++","javascript","typescript","sql","bash",
    "react","next.js","node.js","django","flask","fastapi","html","css","tailwind",
    "aws","azure","gcp","docker","kubernetes","terraform","ansible","grafana","prometheus",
    "opentelemetry","loki","tempo","mimir","git","github actions","cicd","ci/cd",
    "numpy","pandas","scikit-learn","sklearn","pytorch","tensorflow","hugging face",
    "transformers","nlp","llm","rag","vector db","faiss","pinecone","weaviate",
    "mysql","postgresql","mongodb","redis","kafka","rabbitmq",
    "pytest","playwright","selenium","performance testing","oauth","oidc","jwt","grpc","microservices"
]
ALIASES = {"sklearn":"scikit-learn","ci/cd":"cicd","k8s":"kubernetes","js":"javascript","ts":"typescript"}

def _normalize(s:str)->str:
    s = s.lower().replace("\u00a0"," ")
    return re.sub(r"\s+"," ", s)

def _tokens(s:str):
    s = s.translate(str.maketrans("", "", "".join(ch for ch in string.punctuation if ch not in "+.#")))
    return re.findall(r"[a-z0-9+.#]+", s)

def extract_text_from_pdf(path:str)->str:
    doc = fitz.open(path)
    text = "\n".join(p.get_text("text") for p in doc)
    doc.close()
    return _normalize(text)

def tfidf_similarity(a:str,b:str)->float:
    v = TfidfVectorizer(stop_words="english", max_features=5000, ngram_range=(1,2))
    X = v.fit_transform([a,b])
    return round(float(cosine_similarity(X[0:1], X[1:2])[0,0])*100,2)

def extract_skills(text:str)->set:
    toks = set(_tokens(text))
    present = set()
    for sk in SKILL_DB:
        cand = process.extractOne(sk, toks, scorer=fuzz.token_set_ratio, score_cutoff=87)
        if cand: present.add(ALIASES.get(sk, sk))
    return present

SUGGESTION_MAP = {
    "python":"Add 1–2 quantified Python bullets (API/ETL) with metrics.",
    "react":"Link a deployed React/Next.js app; mention perf/SEO gains.",
    "docker":"Add multi‑stage Dockerfile and image size in a bullet.",
    "kubernetes":"Show HPA + probes in a repo; 1 line on autoscaling.",
    "terraform":"Include IaC for one service; remote backend + workspaces.",
    "github actions":"Add CI badge; steps: lint/test/build/deploy.",
    "pandas":"Add EDA/feature‑eng notebook; 2 insights.",
    "scikit-learn":"Baseline model with ROC‑AUC/F1 + CV.",
    "pytorch":"Fine‑tune tiny model; log latency/throughput.",
    "transformers":"Small text‑cls/NER with dataset + scores.",
    "llm":"RAG demo; note context, retrieval quality, guardrails.",
    "opentelemetry":"Trace a request across services; screenshot link.",
    "prometheus":"Expose /metrics; custom counters + Grafana panel.",
}

def compare_resume_with_jd(resume_pdf:str, jd_text:str):
    resume_text = extract_text_from_pdf(resume_pdf)
    jd_text = _normalize(jd_text)

    sim = tfidf_similarity(resume_text, jd_text)
    r_sk = extract_skills(resume_text)
    j_sk = extract_skills(jd_text)

    matched = sorted(r_sk & j_sk)
    missing = sorted(j_sk - r_sk)
    extras  = sorted(r_sk - j_sk)

    suggestions = {sk: SUGGESTION_MAP.get(sk, f"Add a concise bullet proving {sk} with impact metric.")
                   for sk in missing}

    return {
        "similarity": sim,
        "matched": matched,
        "missing": missing,
        "extras": extras,
        "suggestions": suggestions
    }
