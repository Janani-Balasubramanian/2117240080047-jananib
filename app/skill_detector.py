import json
import os
from pathlib import Path

SKILL_CATALOG_PATH = Path(__file__).resolve().parent / "skill_catalog.json"

SKILL_KEYWORDS = {
    "Python": [".py", "python"],
    "Java": [".java", "java"],
    "JavaScript": ["javascript", ".js"],
    "TypeScript": ["typescript", ".ts", ".tsx"],
    "C++": [".cpp", ".cc", ".cxx", "c++"],
    "C#": [".cs", "c#"],
    "Go": ["golang", ".go"],
    "Kotlin": ["kotlin", ".kt", ".kts"],
    "React": ["react"],
    "Angular": ["angular"],
    "Vue.js": ["vue", ".vue"],
    "Next.js": ["next.js", ".next", "next"],
    "HTML/CSS": ["html", "css"],
    "Tailwind CSS": ["tailwind"],
    "Responsive Web Design": ["responsive", "mobile first", "responsive design"],
    "Node.js": ["node", "node.js"],
    "Express.js": ["express"],
    "FastAPI": ["fastapi"],
    "Django": ["django"],
    "Flask": ["flask"],
    "Spring Boot": ["springboot", "spring boot"],
    "REST API Design": ["rest api", "restful"],
    "GraphQL": ["graphql"],
    "PostgreSQL": ["postgresql", "psycopg2"],
    "MySQL": ["mysql"],
    "MongoDB": ["mongodb"],
    "Redis": ["redis"],
    "SQLite": ["sqlite3"],
    "SQL": ["sql"],
    "AWS": ["aws", "amazon web services"],
    "Microsoft Azure": ["azure"],
    "Google Cloud Platform": ["gcp", "google cloud", "google cloud platform"],
    "Firebase": ["firebase"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes"],
    "CI/CD": ["ci/cd", "continuous integration", "continuous deployment"],
    "Git": ["git", ".git"],
    "Linux": ["linux"],
    "Terraform": ["terraform"],
    "Nginx": ["nginx"],
    "Machine Learning": ["machine learning", "ml"],
    "Data Analysis": ["data analysis", "analysis"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["torch"],
    "React Native": ["react native"],
    "Flutter": ["flutter"],
    "Android Development": ["android development", "android"],
    "Cybersecurity": ["cybersecurity", "security"],
}


def load_skill_catalog():
    try:
        with open(SKILL_CATALOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def add_skill_to_catalog(skill_name: str) -> str:
    """
    Add a new skill to the catalog file and return the new skill_id.
    """
    try:
        catalog = load_skill_catalog()
    except Exception:
        catalog = []

    # Determine next numeric id
    max_num = 0
    for item in catalog:
        sid = item.get("skill_id", "")
        if sid.startswith("sk-"):
            try:
                n = int(sid.split("-")[-1])
                if n > max_num:
                    max_num = n
            except Exception:
                continue

    new_num = max_num + 1
    new_id = f"sk-{new_num:03d}"

    new_entry = {"skill_id": new_id, "skill_name": skill_name, "category": "Uncategorized"}
    catalog.append(new_entry)

    try:
        with open(SKILL_CATALOG_PATH, "w", encoding="utf-8") as f:
            json.dump(catalog, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

    return new_id


def detect_skills(file_paths):
    detected = {}
    catalog = load_skill_catalog()
    skill_names = {item["skill_name"] for item in catalog}

    for file_path in file_paths:
        filename = os.path.basename(file_path).lower()

        if filename.endswith(".py") and "Python" in skill_names:
            detected["Python"] = {
                "confidence": 0.95,
                "reason": "Python source file detected."
            }

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read().lower()

                for skill, keywords in SKILL_KEYWORDS.items():
                    for keyword in keywords:
                        if keyword in content or keyword in filename:
                            # If the skill isn't listed in the catalog, add it.
                            if skill not in skill_names:
                                try:
                                    new_id = add_skill_to_catalog(skill)
                                    # refresh catalog set
                                    catalog = load_skill_catalog()
                                    skill_names = {item["skill_name"] for item in catalog}
                                except Exception:
                                    new_id = None

                            detected[skill] = {
                                "confidence": 0.90,
                                "reason": f"Detected keyword '{keyword}'."
                            }
                            # include the skill_id if available
                            if skill in skill_names:
                                # find id
                                sid = next((i.get("skill_id") for i in catalog if i.get("skill_name") == skill), None)
                                if sid:
                                    detected[skill]["skill_id"] = sid
                            break

        except Exception:
            continue

    return detected