import os
from typing import Optional
from dotenv import load_dotenv


load_dotenv()


try:
import google.generativeai as genai
except Exception: # package may be omitted
genai = None




_API_KEY = os.getenv("GEMINI_API_KEY")




def gemini_suggestions(resume_text: str, jd_text: str, missing_skills: list[str]) -> Optional[str]:
if not (_API_KEY and genai):
return None
genai.configure(api_key=_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
prompt = (
"You are an expert resume coach. Given a resume and a job description, "
"list at most 6 crisp, actionable suggestions (bulleted) to close gaps.\n\n"
f"Missing skills (heuristic): {', '.join(missing_skills)}\n\n"
"Resume:\n" + resume_text[:12000] + "\n\nJD:\n" + jd_text[:8000]
)
resp = model.generate_content(prompt)
try:
return resp.text.strip()
except Exception:
return None