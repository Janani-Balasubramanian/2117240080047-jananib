from typing import Dict, List
from app.models import Question

DEFAULT_QUESTIONS: Dict[str, Dict[str, List[str]]] = {
    "Python": {
        "conceptual": [
            {
                "text": "Explain how Python manages memory and garbage collection.",
                "key_points": ["Reference counting", "Garbage collector", "Memory leak prevention"]
            },
            {
                "text": "How do you structure reusable code in Python projects using modules and packages?",
                "key_points": ["Modules and imports", "Package structure", "__init__.py purpose"]
            },
            {
                "text": "What are decorators in Python and how do you use them?",
                "key_points": ["Function wrapping", "Preserving function metadata with functools.wraps", "Real-world use cases"]
            }
        ],
        "codebase_specific": [
            {
                "text": "Walk us through the entry point of your application. What does it initialize and in what order?",
                "key_points": ["Main module flow", "Dependency initialization", "Configuration loading"]
            },
            {
                "text": "How do you handle errors and edge cases in your Python code? Show an example from your project.",
                "key_points": ["Exception handling strategy", "Logging approach", "Specific code examples"]
            }
        ]
    },
    "FastAPI": {
        "conceptual": [
            {
                "text": "How do you define request validation and response models in FastAPI?",
                "key_points": ["Pydantic models", "Type hints", "Automatic OpenAPI docs"]
            },
            {
                "text": "Explain the difference between path parameters, query parameters, and body parameters in FastAPI.",
                "key_points": ["Parameter types", "Validation rules", "Usage patterns"]
            }
        ],
        "codebase_specific": [
            {
                "text": "Describe the API endpoints in your project. What does each endpoint do and what models does it use?",
                "key_points": ["Endpoint purpose", "Request/response models", "HTTP methods and status codes"]
            },
            {
                "text": "How did you organize your FastAPI routes? Show the structure and explain your design choice.",
                "key_points": ["Router organization", "File structure", "Separation of concerns"]
            }
        ]
    },
    "Django": {
        "conceptual": [
            {
                "text": "How do you define models and relationships in Django?",
                "key_points": ["Model fields", "Foreign keys and many-to-many", "Meta options"]
            },
            {
                "text": "What is the Django ORM and how do you use it to query data?",
                "key_points": ["QuerySet API", "Filter and exclude", "Lazy evaluation"]
            }
        ],
        "codebase_specific": [
            {
                "text": "Walk through the models.py file in your project. What entities did you define and why?",
                "key_points": ["Entity definitions", "Relationship design", "Business logic"]
            }
        ]
    },
    "Flask": {
        "conceptual": [
            {
                "text": "How do you create and register blueprints in Flask?",
                "key_points": ["Blueprint creation", "URL prefix", "Application structure"]
            },
            {
                "text": "How do you secure a Flask application with authentication?",
                "key_points": ["Session management", "Password hashing", "Authorization checks"]
            }
        ],
        "codebase_specific": [
            {
                "text": "Show your application factory pattern in Flask. How do you structure your app initialization?",
                "key_points": ["App factory", "Configuration", "Extension registration"]
            }
        ]
    },
    "PostgreSQL": {
        "conceptual": [
            {
                "text": "How do you model relationships and design indexes in PostgreSQL?",
                "key_points": ["Foreign keys", "Indexes for performance", "Constraints"]
            },
            {
                "text": "Explain normalization and how you apply it in your database design.",
                "key_points": ["Normal forms", "Denormalization trade-offs", "Query optimization"]
            }
        ],
        "codebase_specific": [
            {
                "text": "Show us your database schema. What tables did you create and what relationships exist?",
                "key_points": ["Table design", "Foreign key relationships", "Data types chosen"]
            }
        ]
    },
    "MySQL": {
        "conceptual": [
            {
                "text": "How do you connect a Python application to a MySQL database?",
                "key_points": ["Connection pooling", "Drivers (e.g., PyMySQL, mysql-connector)", "Error handling"]
            },
            {
                "text": "How do you optimize MySQL queries for performance?",
                "key_points": ["Indexes", "Query execution plans", "Join optimization"]
            }
        ],
        "codebase_specific": [
            {
                "text": "Show the database initialization and migration strategy in your project.",
                "key_points": ["Schema creation", "Migration tools", "Seed data"]
            }
        ]
    },
    "MongoDB": {
        "conceptual": [
            {
                "text": "How does MongoDB differ from relational databases like PostgreSQL?",
                "key_points": ["Document-oriented", "BSON format", "Flexible schema"]
            },
            {
                "text": "How do you model relationships in MongoDB?",
                "key_points": ["Embedding vs referencing", "Denormalization", "Query patterns"]
            }
        ],
        "codebase_specific": [
            {
                "text": "Describe the document structure in your MongoDB collections. Why did you choose this design?",
                "key_points": ["Document schema", "Embedding strategy", "Query patterns used"]
            }
        ]
    },
    "Docker": {
        "conceptual": [
            {
                "text": "What is Docker and why would you use containers instead of virtual machines?",
                "key_points": ["Container isolation", "Image layers", "Resource efficiency"]
            },
            {
                "text": "How do you compose multiple services with docker-compose?",
                "key_points": ["Service definitions", "Networking", "Volume management"]
            }
        ],
        "codebase_specific": [
            {
                "text": "Show us your Dockerfile. What are the key steps and why did you structure it this way?",
                "key_points": ["Base image choice", "Dependency installation", "Entry point"]
            },
            {
                "text": "How do you deploy your application with Docker? What environment variables are needed?",
                "key_points": ["Container orchestration", "Port mapping", "Configuration"]
            }
        ]
    },
    "React": {
        "conceptual": [
            {
                "text": "What is the virtual DOM and why does React use it?",
                "key_points": ["Diffing algorithm", "Performance benefits", "Reconciliation"]
            },
            {
                "text": "Explain React hooks and their benefits over class components.",
                "key_points": ["useState", "useEffect", "Custom hooks"]
            }
        ],
        "codebase_specific": [
            {
                "text": "Show a key component from your React application. How does it manage state and side effects?",
                "key_points": ["Component structure", "Hook usage", "Props and state"]
            }
        ]
    },
    "Git": {
        "conceptual": [
            {
                "text": "How do you manage branches and merge changes with Git?",
                "key_points": ["Branch creation", "Merge strategies", "Pull requests"]
            },
            {
                "text": "How do you resolve merge conflicts in Git?",
                "key_points": ["Conflict markers", "Manual resolution", "Merge tools"]
            }
        ],
        "codebase_specific": [
            {
                "text": "Walk us through your Git commit history. What is your branching strategy?",
                "key_points": ["Commit messages", "Feature branches", "Merge practices"]
            }
        ]
    },
}


def generate_questions(
    project_title: str,
    detected_skills: Dict[str, dict],
    project_description: str = "",
    project_outcomes: str = "",
    questions_per_skill: int = 2,
) -> List[Dict[str, any]]:
    """
    Generate interview questions per detected skill.
    Returns a list of question objects with focus and key points.
    """
    if not detected_skills:
        return []

    all_questions = []

    for skill_name in detected_skills.keys():
        skill_data = DEFAULT_QUESTIONS.get(skill_name, {})
        
        conceptual_qs = skill_data.get("conceptual", [])
        codebase_qs = skill_data.get("codebase_specific", [])
        
        questions_to_add = []
        
        # Balance between conceptual and codebase-specific
        if questions_per_skill == 1:
            questions_to_add = conceptual_qs[:1]
        elif questions_per_skill == 2:
            questions_to_add = conceptual_qs[:1] + codebase_qs[:1]
        else:
            # For more than 2, mix them
            half = questions_per_skill // 2
            questions_to_add = (conceptual_qs[:half] + codebase_qs[:half])[:questions_per_skill]
        
        for i, q_data in enumerate(questions_to_add):
            focus = "conceptual" if i == 0 else "codebase_specific"
            if i > 0 and skill_data.get("codebase_specific"):
                focus = "codebase_specific"
            elif i == 0 and skill_data.get("conceptual"):
                focus = "conceptual"
            
            question_obj = {
                "skill_name": skill_name,
                "question_text": q_data.get("text", ""),
                "question_focus": focus,
                "expected_key_points": q_data.get("key_points", [])
            }
            all_questions.append(question_obj)
        
        # Fallback if not enough questions
        if len(questions_to_add) < questions_per_skill:
            fallback_qs = [
                f"What challenges did you face when using {skill_name}?",
                f"How would you improve your {skill_name} implementation?",
                f"Explain your experience with {skill_name} in this project.",
            ]
            
            for fallback in fallback_qs:
                if len(questions_to_add) + len([q for q in all_questions if q['skill_name'] == skill_name]) < questions_per_skill:
                    all_questions.append({
                        "skill_name": skill_name,
                        "question_text": fallback,
                        "question_focus": "codebase_specific",
                        "expected_key_points": ["Project-specific challenges", "Learning outcomes", "Improvement areas"]
                    })

    return all_questions
