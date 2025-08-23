from pydantic import BaseModel
from typing import List, Optional, Dict


class MatchRequest(BaseModel):
jd_text: str


class UploadResponse(BaseModel):
resume_text: str
meta: Dict[str, str]


class MatchResponse(BaseModel):
score_overall: float
scores: Dict[str, float]
extracted_skills: List[str]
jd_skills: List[str]
matched_skills: List[str]
missing_skills: List[str]
suggestions: List[str]
llm_suggestions: Optional[str] = None