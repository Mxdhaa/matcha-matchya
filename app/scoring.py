from typing import List, Dict
from rapidfuzz import fuzz
from .utils import tokens




def coverage_score(resume_skills: List[str], jd_skills: List[str]) -> float:
rs, js = set(resume_skills), set(jd_skills)
if not js:
return 0.0
covered = len(rs & js) / len(js)
return round(100 * covered, 2)




def fuzzy_overlap_score(resume_text: str, jd_text: str) -> float:
# Ratio over token‑sorted strings
return round(float(fuzz.token_sort_ratio(resume_text, jd_text)), 2)




def keyword_hit_rate(resume_text: str, jd_text: str, jd_skills: List[str]) -> float:
rtoks = set(tokens(resume_text))
hits = 0
for k in jd_skills:
ktoks = set(tokens(k))
if ktoks.issubset(rtoks):
hits += 1
if not jd_skills:
return 0.0
return round(100 * hits / len(jd_skills), 2)




def overall(scores: Dict[str, float]) -> float:
# weighted blend
w = {"coverage": 0.45, "fuzzy": 0.35, "khr": 0.20}
s = w["coverage"] * scores["coverage"] + w["fuzzy"] * scores["fuzzy"] + w["khr"] * scores["khr"]
return round(s, 2)