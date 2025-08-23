from typing import List, Set
import spacy
from .utils import normalize, tokens, uniq


# Try to load a small English model; fall back to blank if unavailable
try:
	nlp = spacy.load("en_core_web_sm")
except Exception:
	nlp = spacy.blank("en")


# Minimal skill KB (extend as needed)
SKILL_KB = {
# languages & frameworks
"python", "c++", "java", "javascript", "typescript", "html", "css", "sql", "mongodb", "postgresql",
"react", "next.js", "node", "tailwind", "socket.io",
# ml/ai
"pytorch", "tensorflow", "tesseract", "ocr", "opencv", "mediapipe", "hugging face", "transformers",
"bert", "gnn", "gatconv", "spacy", "llm", "nlp", "gemini", "claude",
# tools
"git", "vercel", "rest api", "jira", "supabase",
}




_DEF_MIN_LEN = 2




def extract_skills(text: str) -> List[str]:
	text_n = normalize(text)
	doc = nlp(text_n)

	# exact KB matches (unigrams/bigrams)
	words = tokens(text_n)
	cands = set()
	for i, w in enumerate(words):
		if w in SKILL_KB:
			cands.add(w)
		if i + 1 < len(words):
			bg = f"{w} {words[i+1]}"
			if bg in SKILL_KB:
				cands.add(bg)

	# noun chunks as skills (fallback)
	if hasattr(doc, "noun_chunks"):
		for nc in doc.noun_chunks:
			s = nc.text.strip()
			if len(s) >= _DEF_MIN_LEN:
				cands.add(s)

	# simple cleanup
	return uniq(sorted(cands))