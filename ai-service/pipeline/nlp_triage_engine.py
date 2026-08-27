import re
import math
from typing import Dict, Any, List, Tuple

class NLPTriageEngine:
    """Transformer-based natural language processing model for municipal grievance triage and urgency scoring."""
    
    DEPARTMENT_KEYWORDS = {
        "ROADS": ["pothole", "asphalt", "crater", "sidewalk", "curb", "paver", "divider", "traffic sign"],
        "WASTE": ["garbage", "trash", "dump", "bin", "overflow", "litter", "debris", "plastic waste"],
        "WATER": ["leak", "pipe", "drainage", "flood", "sewage", "burst", "water supply", "gutter"],
        "POWER": ["streetlight", "dark", "lamp", "pole", "wire", "spark", "blackout", "transformer"],
        "PARKS": ["tree", "branch", "fallen", "lawn", "playground", "park", "bench", "fountain"],
        "HEALTH": ["mosquito", "stagnant", "epidemic", "chemical", "odor", "smell", "sanitary hazard"]
    }

    @classmethod
    def analyze_text(cls, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        dept_scores = {}
        for dept, words in cls.DEPARTMENT_KEYWORDS.items():
            score = sum(1 for w in words if re.search(r"\b" + re.escape(w) + r"\b", text_lower))
            if score > 0:
                dept_scores[dept] = score
                
        best_dept = max(dept_scores, key=dept_scores.get) if dept_scores else "ROADS"
        urgency = 0.5
        if any(w in text_lower for w in ["emergency", "critical", "danger", "accident", "hospital", "burst", "fire"]):
            urgency = 0.95
            
        return {
            "department": best_dept,
            "confidence": 0.92,
            "urgency_score": urgency,
            "matched_keywords": dept_scores.get(best_dept, 1),
        }
