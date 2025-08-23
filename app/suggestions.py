from typing import List




def generate_suggestions(missing_skills: List[str]) -> List[str]:
if not missing_skills:
return ["Great match! Consider adding quantified impact bullets and links to live demos."]
out = [
"Prioritize learning or showcasing the following to improve JD match:",
]
for sk in missing_skills[:15]:
out.append(f"• Add a bullet or mini‑project demonstrating {sk} (coursework, GitHub repo, or certification).")
out.append("• Mirror JD keywords in your resume (skills section + bullet points) where truthful.")
out.append("• Place the most relevant skills/projects in the top third of your resume.")
return out