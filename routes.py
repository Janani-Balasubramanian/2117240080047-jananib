from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import time
from app.models import (
    AnalysisResponse, 
    SkillEvaluation, 
    EvaluationReport,
    EvaluationSummary,
    Metadata,
    Question
)
from app.utils import get_all_files, read_file_content
from app.zip_parser import save_zip, extract_zip
from app.skill_detector import detect_skills
from app.ai_generator import generate_questions
from app.confidence_scorer import rank_detected_skills
from app.outcome_evaluator import parse_outcomes, evaluate_outcomes

router = APIRouter()


@router.post("/analyze-submission", response_model=AnalysisResponse)
async def analyze_submission(
    project_title: str = Form(...),
    project_description: str = Form(""),
    project_outcomes: str = Form(...),
    questions_per_skill: int = Form(2),
    zip_file: UploadFile = File(...)
):
    processing_start = time.time()
    extraction_start = time.time()
    
    if zip_file.content_type not in ["application/zip", "application/x-zip-compressed", "multipart/form-data"]:
        raise HTTPException(status_code=400, detail="Uploaded file must be a ZIP archive.")

    # Save and extract ZIP
    zip_path = save_zip(zip_file)
    extracted_folder = extract_zip(zip_path)
    
    extraction_time_ms = (time.time() - extraction_start) * 1000
    
    # Get all files from extracted folder
    files = get_all_files(extracted_folder)
    if not files:
        raise HTTPException(status_code=400, detail="The uploaded ZIP archive contains no supported files.")
    
    # Read file contents for analysis
    files_content = {}
    for file_path in files[:50]:  # Limit to first 50 files for performance
        try:
            content = read_file_content(file_path)
            if content:
                files_content[file_path] = content
        except Exception:
            continue
    
    # Detect skills from files
    detected_skills_dict = detect_skills(files)
    
    # Rank skills by confidence
    suggested_skills = rank_detected_skills(detected_skills_dict, files_content)
    
    # Parse project outcomes
    parsed_outcomes = parse_outcomes(project_outcomes)
    
    # Evaluate outcomes against codebase
    detected_skill_names = [s["skill_name"] for s in suggested_skills]
    outcome_evals, narrative, alignment_score, strengths, gaps = evaluate_outcomes(
        parsed_outcomes,
        files_content,
        detected_skill_names
    )
    
    # Generate questions for each detected skill
    all_questions_data = generate_questions(
        project_title,
        detected_skills_dict,
        project_description=project_description,
        project_outcomes=project_outcomes,
        questions_per_skill=questions_per_skill,
    )
    
    # Organize questions by skill
    skills_questions = {}
    for q_data in all_questions_data:
        skill_name = q_data["skill_name"]
        if skill_name not in skills_questions:
            skills_questions[skill_name] = []
        
        question = Question(
            question_text=q_data["question_text"],
            question_focus=q_data["question_focus"],
            expected_key_points=q_data["expected_key_points"]
        )
        skills_questions[skill_name].append(question)
    
    # Build skill evaluations
    skill_evals = []
    for skill_name in detected_skill_names:
        questions = skills_questions.get(skill_name, [])
        skill_eval = SkillEvaluation(
            skill_name=skill_name,
            questions=questions
        )
        skill_evals.append(skill_eval)
    
    # Build summary
    summary = EvaluationSummary(
        overall_alignment=("strong" if alignment_score >= 0.8 else "partial" if alignment_score >= 0.5 else "weak"),
        alignment_score=alignment_score,
        narrative=narrative,
        outcome_evaluation=outcome_evals,
        strengths=strengths,
        gaps=gaps
    )
    
    # Build metadata
    metadata = Metadata(
        files_analyzed=len(files_content),
        extraction_time_ms=extraction_time_ms,
        model_tokens_used=0  # Local generation, no tokens
    )
    
    # Build evaluation report
    evaluation_report = EvaluationReport(
        skills=skill_evals,
        summary=summary,
        metadata=metadata
    )
    
    processing_time_ms = (time.time() - processing_start) * 1000
    
    return AnalysisResponse(
        project_title=project_title,
        suggested_skills=suggested_skills,
        evaluation_report=evaluation_report,
        processing_time_ms=processing_time_ms
    )
