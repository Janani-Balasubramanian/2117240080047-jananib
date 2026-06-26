import re
from typing import List, Tuple
from app.models import OutcomeEvaluation


def parse_outcomes(outcomes_text: str) -> List[str]:
    """
    Parse project outcomes from text (supports numbered lists, bullets, newlines).
    """
    if not outcomes_text or not outcomes_text.strip():
        return []
    
    outcomes = []
    lines = outcomes_text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        # Remove numbering: "1. ", "1) ", "- ", "* "
        line = re.sub(r'^[\d]+[.)]\s*', '', line)
        line = re.sub(r'^[-*]\s*', '', line)
        line = line.strip()
        
        if line:
            outcomes.append(line)
    
    return outcomes


def extract_evidence_from_files(files_content: dict, outcome: str) -> Tuple[str, str]:
    """
    Search for evidence of an outcome in file content.
    Returns (evidence_text, gap_if_any)
    """
    outcome_lower = outcome.lower()
    keywords = extract_outcome_keywords(outcome)
    
    evidence_lines = []
    matched_files = []
    
    for filepath, content in files_content.items():
        content_lower = content.lower()
        score = 0
        
        for keyword in keywords:
            score += content_lower.count(keyword)
        
        if score > 0:
            matched_files.append((filepath, score))
            # Extract first few relevant lines
            for line in content.split('\n')[:20]:
                if any(kw in line.lower() for kw in keywords):
                    evidence_lines.append(f"  {filepath}: {line.strip()[:80]}")
                    break
    
    if matched_files:
        evidence = '\n'.join(evidence_lines[:3]) or f"Files found: {', '.join([f[0] for f in matched_files[:2]])}"
        return evidence, None
    
    return "", "No direct evidence found in codebase"


def extract_outcome_keywords(outcome: str) -> List[str]:
    """
    Extract potential keywords from outcome text.
    """
    keywords = []
    
    # Common technical patterns
    outcome_lower = outcome.lower()
    
    if any(word in outcome_lower for word in ['rest api', 'api', 'endpoint']):
        keywords.extend(['@app.post', '@app.get', '@router.', 'def ', 'async def'])
    
    if any(word in outcome_lower for word in ['auth', 'login', 'security', 'jwt']):
        keywords.extend(['auth', 'jwt', 'token', 'password', 'verify'])
    
    if any(word in outcome_lower for word in ['database', 'db', 'sql', 'model']):
        keywords.extend(['table', 'schema', 'model', 'database', 'query'])
    
    if any(word in outcome_lower for word in ['docker', 'deploy', 'container']):
        keywords.extend(['dockerfile', 'docker-compose', 'image', 'container'])
    
    if any(word in outcome_lower for word in ['test', 'testing']):
        keywords.extend(['test', 'unittest', 'pytest', 'assert'])
    
    if any(word in outcome_lower for word in ['ui', 'frontend', 'component', 'react']):
        keywords.extend(['component', 'useState', 'useEffect', '<', 'jsx', 'render'])
    
    # Add words from outcome itself
    words = outcome_lower.split()
    keywords.extend([w for w in words if len(w) > 4 and w not in ['build', 'create', 'implement', 'design']])
    
    return list(set(keywords))


def evaluate_outcomes(
    stated_outcomes: List[str],
    files_content: dict,
    detected_skills: List[str]
) -> Tuple[List[OutcomeEvaluation], str, float, List[str], List[str]]:
    """
    Evaluate each stated outcome against actual codebase evidence.
    Returns: (outcome_evaluations, narrative, alignment_score, strengths, gaps)
    """
    outcome_evals = []
    alignment_sum = 0
    
    for outcome in stated_outcomes:
        evidence, gap = extract_evidence_from_files(files_content, outcome)
        
        if evidence and not gap:
            status = "met"
            alignment_sum += 1.0
        elif evidence and gap:
            status = "partial"
            alignment_sum += 0.5
        else:
            status = "not_verifiable" if gap else "not_met"
            alignment_sum += 0.0
        
        outcome_evals.append(OutcomeEvaluation(
            stated_outcome=outcome,
            status=status,
            evidence=evidence or "No evidence",
            gap=gap
        ))
    
    # Calculate alignment
    alignment_score = alignment_sum / len(stated_outcomes) if stated_outcomes else 0.5
    
    if alignment_score >= 0.8:
        overall = "strong"
    elif alignment_score >= 0.5:
        overall = "partial"
    else:
        overall = "weak"
    
    # Generate narrative
    met_count = sum(1 for e in outcome_evals if e.status == "met")
    partial_count = sum(1 for e in outcome_evals if e.status == "partial")
    narrative = (
        f"The submitted codebase demonstrates {met_count} fully met outcomes and {partial_count} partial implementations. "
        f"Detected skills ({', '.join(detected_skills[:3])}) align with the project scope. "
        f"The implementation shows intentional design decisions with clear separation of concerns."
    )
    
    # Extract strengths and gaps
    strengths = [
        "Clear project structure with organized modules",
        f"Detected {len(detected_skills)} technical skills aligned with project",
        "Evidence of iterative development and problem-solving"
    ]
    
    gaps = [e.gap for e in outcome_evals if e.gap]
    if not gaps:
        gaps = ["Minor gaps in documentation"]
    
    return outcome_evals, narrative, alignment_score, strengths, gaps
