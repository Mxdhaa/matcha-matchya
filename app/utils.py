import re
from typing import Iterable, List
_WS = re.compile(r"\s+")
STOPWORDS = set(
"""
a an the and or of to in for with on at from by as is are was were be been being have has had do does did this that those these you your we our it its their his her they them i me my
""".split()
)
punct_tbl = str.maketrans({c: " " for c in "!@#$%^&*()[]{};:'\",.<>/?`~|\\-+="})
def normalize(text: str) -> str:
	text = text.lower().translate(punct_tbl)
	text = _WS.sub(" ", text).strip()
	return text

def tokens(text: str) -> List[str]:
	return [t for t in normalize(text).split() if t and t not in STOPWORDS]

def uniq(seq: Iterable[str]) -> List[str]:
	seen, out = set(), []
	for s in seq:
		if s not in seen:
			seen.add(s)
			out.append(s)
	return out
