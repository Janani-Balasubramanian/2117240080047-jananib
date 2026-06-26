import json
from pathlib import Path
from typing import List, Dict, Tuple


def load_skill_catalog() -> dict:
    """Load skill catalog and return as dict keyed by skill name."""
    catalog_path = Path(__file__).resolve().parent / "skill_catalog.json"
    try:
        with open(catalog_path, "r", encoding="utf-8") as f:
            catalog = json.load(f)
            return {item["skill_name"]: item["skill_id"] for item in catalog}
    except FileNotFoundError:
        return {}


def calculate_skill_confidence(
    skill_name: str,
    files_content: dict,
    detected_keywords: dict
) -> Tuple[float, str]:
    """
    Calculate confidence score for a skill (0-1) and return rationale.
    """
    skill_lower = skill_name.lower()
    
    # Count occurrences in files
    total_matches = 0
    file_matches = []
    
    for filepath, content in files_content.items():
        content_lower = content.lower()
        matches = content_lower.count(skill_lower)
        
        # Also check for common patterns
        if skill_name == "Python":
            matches += content_lower.count(".py") * 2
            matches += content_lower.count("import ")
        elif skill_name == "FastAPI":
            matches += content_lower.count("@app.") * 2
            matches += content_lower.count("@router.") * 2
        elif skill_name == "Docker":
            matches += content_lower.count("dockerfile") * 3
            matches += content_lower.count("docker-compose") * 3
        elif skill_name == "PostgreSQL":
            matches += content_lower.count("postgresql") * 2
            matches += content_lower.count("engine = create_engine") * 2
        
        if matches > 0:
            file_matches.append((filepath, matches))
            total_matches += matches
    
    # Normalize confidence
    if total_matches == 0:
        confidence = 0.0
        rationale = f"No evidence of {skill_name} found in codebase"
    elif total_matches <= 2:
        confidence = 0.5
        rationale = f"Minimal evidence of {skill_name}; mentioned in {len(file_matches)} file(s)"
    elif total_matches <= 5:
        confidence = 0.7
        rationale = f"Moderate use of {skill_name}; detected in {len(file_matches)} file(s) with {total_matches} indicators"
    elif total_matches <= 15:
        confidence = 0.85
        rationale = f"Strong use of {skill_name}; extensively referenced across {len(file_matches)} file(s)"
    else:
        confidence = 0.95
        rationale = f"{skill_name} is a core component; heavily used throughout the codebase"
    
    return confidence, rationale


def rank_detected_skills(
    detected_skills_dict: Dict[str, dict],
    files_content: dict
) -> List[Dict]:
    """
    Rank detected skills by confidence and add skill IDs.
    """
    catalog = load_skill_catalog()
    ranked = []
    
    for skill_name, skill_info in detected_skills_dict.items():
        if skill_name not in catalog:
            continue
        
        confidence, rationale = calculate_skill_confidence(skill_name, files_content, skill_info)
        
        # Only include skills with meaningful confidence
        if confidence >= 0.5:
            ranked.append({
                "skill_id": catalog[skill_name],
                "skill_name": skill_name,
                "confidence": confidence,
                "rationale": rationale
            })
    
    # Sort by confidence descending
    ranked.sort(key=lambda x: x["confidence"], reverse=True)
    
    return ranked
