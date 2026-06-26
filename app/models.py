from pydantic import BaseModel
from typing import Dict, List, Optional, Literal


class Question(BaseModel):
    question_text: str
    question_focus: Literal["conceptual", "codebase_specific"]
    expected_key_points: List[str]


class SkillEvaluation(BaseModel):
    skill_name: str
    questions: List[Question]


class OutcomeEvaluation(BaseModel):
    stated_outcome: str
    status: Literal["met", "partial", "not_met", "not_verifiable"]
    evidence: str
    gap: Optional[str] = None


class EvaluationSummary(BaseModel):
    overall_alignment: Literal["strong", "partial", "weak"]
    alignment_score: float
    narrative: str
    outcome_evaluation: List[OutcomeEvaluation]
    strengths: List[str]
    gaps: List[str]


class Metadata(BaseModel):
    files_analyzed: int
    extraction_time_ms: float
    model_tokens_used: int


class SuggestedSkill(BaseModel):
    skill_id: str
    skill_name: str
    confidence: float
    rationale: str


class EvaluationReport(BaseModel):
    skills: List[SkillEvaluation]
    summary: EvaluationSummary
    metadata: Metadata


class AnalysisResponse(BaseModel):
    project_title: str
    suggested_skills: List[SuggestedSkill]
    evaluation_report: EvaluationReport
    processing_time_ms: float
