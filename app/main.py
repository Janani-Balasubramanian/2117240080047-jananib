from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.routes import router

app = FastAPI(
    title="Project Submission AI Analyzer",
    version="1.0.0",
    description="Analyzes project ZIP files and generates skill evaluations."
)

app.include_router(router)

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Project Submission AI Analyzer</title>
        <style>
            body { font-family: Arial, sans-serif; background: #eef2ff; margin: 0; padding: 0; color: #111827; }
            .container { max-width: 1000px; margin: 40px auto; padding: 32px; background: #ffffff; border-radius: 24px; box-shadow: 0 18px 40px rgba(15, 23, 42, 0.12); }
            h1 { margin-top: 0; font-size: 2.4rem; }
            h3 { margin-top: 32px; font-size: 1.4rem; color: #1f2937; }
            h4 { margin-top: 16px; font-size: 1.1rem; color: #374151; }
            p { line-height: 1.7; }
            label { display: block; margin-top: 20px; font-weight: 600; }
            input, textarea, select { width: 100%; margin-top: 8px; padding: 14px 16px; border: 1px solid #d1d5db; border-radius: 14px; font-size: 1rem; background: #f9fafb; box-sizing: border-box; }
            button { margin-top: 24px; padding: 14px 20px; border: none; border-radius: 14px; background: #4f46e5; color: #ffffff; font-weight: 700; cursor: pointer; transition: background 0.2s ease; }
            button:hover { background: #4338ca; }
            .result-box { margin-top: 34px; padding: 24px; background: #eef2ff; border-radius: 18px; border: 1px solid #dbeafe; }
            .result-box h2 { margin-top: 0; }
            .field-note { color: #6b7280; font-size: 0.95rem; margin-top: 6px; }
            .skill-list, .question-list { margin: 12px 0; padding-left: 1.4rem; }
            .skill-list li, .question-list li { margin: 8px 0; line-height: 1.6; }
            em { color: #6b7280; font-size: 0.9rem; }
            ul { line-height: 1.8; }
            li { margin: 8px 0; }
            .footer { margin-top: 30px; font-size: 0.95rem; color: #6b7280; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Project Submission AI Analyzer</h1>
            <p>Upload a ZIP of your internship project, then receive detected technical skills and AI-generated interview questions.</p>
            <form id="analysis-form">
                <label for="project_title">Project Title</label>
                <input id="project_title" name="project_title" type="text" placeholder="My Internship Project" required />

                <label for="project_description">Project Description</label>
                <textarea id="project_description" name="project_description" rows="4" placeholder="Describe the project briefly."></textarea>

                <label for="project_outcomes">Project Outcomes</label>
                <textarea id="project_outcomes" name="project_outcomes" rows="3" placeholder="What did you achieve with this project?" required></textarea>

                <label for="questions_per_skill">Questions Per Skill</label>
                <select id="questions_per_skill" name="questions_per_skill">
                    <option value="1">1</option>
                    <option value="2" selected>2</option>
                    <option value="3">3</option>
                    <option value="4">4</option>
                </select>

                <label for="zip_file">Project ZIP File</label>
                <input id="zip_file" name="zip_file" type="file" accept=".zip" required />
                <p class="field-note">Upload a ZIP containing your project files. The analyzer scans inside the extracted folder.</p>

                <button type="submit">Analyze Submission</button>
            </form>

            <div id="result" class="result-box" style="display:none"></div>
            <div class="footer">Powered by FastAPI. Interview questions are generated from local skill templates and project context.</div>
        </div>

        <script>
            const form = document.getElementById('analysis-form');
            const resultBox = document.getElementById('result');

            form.addEventListener('submit', async (event) => {
                event.preventDefault();
                resultBox.style.display = 'block';
                resultBox.textContent = 'Analyzing your submission, please wait...';

                const formData = new FormData(form);

                try {
                    const response = await fetch('/analyze-submission', {
                        method: 'POST',
                        body: formData
                    });

                    if (!response.ok) {
                        const text = await response.text();
                        throw new Error(text || 'Server returned an error.');
                    }

                    const data = await response.json();
                    let html = `<h2>Analysis Results</h2>`;
                    html += `<p><strong>Project:</strong> ${data.project_title}</p>`;
                    html += `<p><strong>Processing Time:</strong> ${data.processing_time_ms.toFixed(2)}ms</p>`;

                    // Suggested Skills
                    html += '<h3>Suggested Skills</h3>';
                    const skills = data.suggested_skills || [];
                    if (skills.length === 0) {
                        html += '<p>No skills detected.</p>';
                    } else {
                        html += '<ul class="skill-list">';
                        for (const skill of skills) {
                            const conf = (skill.confidence * 100).toFixed(0);
                            html += `<li><strong>${skill.skill_name}</strong> (${conf}% confidence): ${skill.rationale}</li>`;
                        }
                        html += '</ul>';
                    }

                    // Evaluation Summary
                    const report = data.evaluation_report || {};
                    const summary = report.summary || {};
                    
                    html += '<h3>Evaluation Summary</h3>';
                    html += `<p><strong>Overall Alignment:</strong> ${summary.overall_alignment} (${(summary.alignment_score * 100).toFixed(1)}%)</p>`;
                    html += `<p><strong>Narrative:</strong> ${summary.narrative}</p>`;

                    // Outcome Evaluation
                    html += '<h3>Outcome Evaluation</h3>';
                    const outcomes = summary.outcome_evaluation || [];
                    if (outcomes.length > 0) {
                        html += '<ul>';
                        for (const outcome of outcomes) {
                            const status_color = outcome.status === 'met' ? '#10b981' : outcome.status === 'partial' ? '#f59e0b' : '#ef4444';
                            html += `<li><strong style="color:${status_color}">[${outcome.status.toUpperCase()}]</strong> ${outcome.stated_outcome}`;
                            if (outcome.evidence) html += `<br/>Evidence: ${outcome.evidence}`;
                            if (outcome.gap) html += `<br/>Gap: ${outcome.gap}`;
                            html += '</li>';
                        }
                        html += '</ul>';
                    }

                    // Strengths and Gaps
                    html += '<h3>Strengths</h3>';
                    const strengths = summary.strengths || [];
                    if (strengths.length > 0) {
                        html += '<ul>';
                        for (const strength of strengths) {
                            html += `<li>${strength}</li>`;
                        }
                        html += '</ul>';
                    }

                    html += '<h3>Gaps Identified</h3>';
                    const gaps = summary.gaps || [];
                    if (gaps.length > 0) {
                        html += '<ul>';
                        for (const gap of gaps) {
                            html += `<li>${gap}</li>`;
                        }
                        html += '</ul>';
                    }

                    // Interview Questions
                    html += '<h3>Interview Questions</h3>';
                    const skillEvals = report.skills || [];
                    if (skillEvals.length === 0) {
                        html += '<p>No questions generated.</p>';
                    } else {
                        for (const skillEval of skillEvals) {
                            html += `<h4>${skillEval.skill_name}</h4>`;
                            html += '<ol class="question-list">';
                            for (const question of skillEval.questions) {
                                html += `<li><strong>[${question.question_focus}]</strong> ${question.question_text}`;
                                if (question.expected_key_points && question.expected_key_points.length > 0) {
                                    html += `<br/><em>Key points: ${question.expected_key_points.join(', ')}</em>`;
                                }
                                html += '</li>';
                            }
                            html += '</ol>';
                        }
                    }

                    // Metadata
                    const metadata = report.metadata || {};
                    html += '<h3>Analysis Metadata</h3>';
                    html += `<p>Files analyzed: ${metadata.files_analyzed} | Extraction time: ${metadata.extraction_time_ms.toFixed(0)}ms</p>`;

                    resultBox.innerHTML = html;
                } catch (error) {
                    resultBox.innerHTML = `<p style="color:#b91c1c"><strong>Error:</strong> ${error.message}</p>`;
                }
            });
        </script>
            <div class="footer">Powered by FastAPI. Interview questions are generated from local skill templates and project context.</div>
        </div>
    </body>
    </html>
    """
