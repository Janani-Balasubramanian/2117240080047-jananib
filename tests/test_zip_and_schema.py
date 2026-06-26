import zipfile
from pathlib import Path

import pytest

from app.models import AnalysisResponse
from app.zip_parser import extract_zip


def write_zip(path: Path, members: list[tuple[str, str]]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name, content in members:
            zf.writestr(name, content)


def test_rejects_zip_entries_with_path_traversal(tmp_path):
    archive = tmp_path / "evil.zip"
    write_zip(archive, [("../outside.txt", "oops")])

    with pytest.raises(ValueError, match="unsafe"):
        extract_zip(str(archive))


def test_analysis_response_schema_accepts_expected_payload():
    payload = {
        "project_title": "Demo App",
        "suggested_skills": [
            {
                "skill_id": "sk-018",
                "skill_name": "FastAPI",
                "confidence": 0.85,
                "rationale": "Strong evidence found in source files.",
            }
        ],
        "evaluation_report": {
            "skills": [
                {
                    "skill_name": "FastAPI",
                    "questions": [
                        {
                            "question_text": "How do you structure FastAPI routes?",
                            "question_focus": "conceptual",
                            "expected_key_points": ["Routing", "Dependency injection"],
                        }
                    ],
                }
            ],
            "summary": {
                "overall_alignment": "strong",
                "alignment_score": 1.0,
                "narrative": "The app demonstrates the requested feature set.",
                "outcome_evaluation": [],
                "strengths": ["Good structure"],
                "gaps": [],
            },
            "metadata": {
                "files_analyzed": 3,
                "extraction_time_ms": 25.0,
                "model_tokens_used": 0,
            },
        },
        "processing_time_ms": 120.0,
    }

    response = AnalysisResponse.model_validate(payload)

    assert response.project_title == "Demo App"
    assert response.suggested_skills[0].skill_name == "FastAPI"
