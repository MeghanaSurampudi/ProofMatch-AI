import io
import re
from typing import Dict, List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SKILL_ALIASES = {
    "Python": ["python"], "SQL": ["sql", "structured query language"],
    "MySQL": ["mysql"], "Java": ["java"], "JavaScript": ["javascript", "js"],
    "HTML": ["html", "html5"], "CSS": ["css", "css3"], "React": ["react", "react.js"],
    "Node.js": ["node.js", "nodejs"], "Express.js": ["express.js", "express"],
    "Flask": ["flask"], "FastAPI": ["fastapi"], "Django": ["django"],
    "Machine Learning": ["machine learning", "ml"], "Deep Learning": ["deep learning"],
    "NLP": ["natural language processing", "nlp"], "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"], "scikit-learn": ["scikit-learn", "sklearn"],
    "Pandas": ["pandas"], "NumPy": ["numpy"], "Generative AI": ["generative ai", "genai"],
    "Large Language Models": ["large language model", "llm", "llms"],
    "Prompt Engineering": ["prompt engineering"], "Git": ["git"], "GitHub": ["github"],
    "Linux": ["linux"], "Docker": ["docker"], "Kubernetes": ["kubernetes"],
    "AWS": ["aws", "amazon web services"], "Azure": ["azure", "microsoft azure"],
    "Google Cloud": ["google cloud", "gcp"], "CI/CD": ["ci/cd", "continuous integration", "continuous deployment"],
    "REST APIs": ["rest api", "rest apis", "restful api"], "Power BI": ["power bi"],
    "Excel": ["excel", "microsoft excel"], "Data Analysis": ["data analysis", "data analytics"],
    "Communication": ["communication", "verbal communication"],
    "Problem Solving": ["problem solving", "problem-solving"],
}

def _contains_phrase(text: str, phrase: str) -> bool:
    pattern = r"(?<![a-z0-9+#.])" + re.escape(phrase.lower()) + r"(?![a-z0-9+#.])"
    return re.search(pattern, text.lower()) is not None

def detect_skills(text: str) -> List[str]:
    return [skill for skill, aliases in SKILL_ALIASES.items()
            if any(_contains_phrase(text, alias) for alias in aliases)]

def _sentences(text: str) -> List[str]:
    return [p.strip() for p in re.split(r"(?<=[.!?])\s+|\n+", text) if len(p.strip()) >= 12]

def _evidence_for_skill(resume: str, skill: str) -> List[str]:
    aliases = SKILL_ALIASES[skill]
    return [sentence for sentence in _sentences(resume)
            if any(_contains_phrase(sentence, alias) for alias in aliases)][:3]

def _similarity(resume: str, job: str) -> float:
    try:
        matrix = TfidfVectorizer(stop_words="english", ngram_range=(1, 2)).fit_transform([resume, job])
        return float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])
    except ValueError:
        return 0.0

def _learning_plan(missing: List[str]) -> List[Dict[str, str]]:
    topics = missing[:7] if missing else ["Validate your evidence", "Practice explaining projects", "Prepare interview examples"]
    if len(topics) < 7:
        topics += ["Build a small portfolio example"] * (7 - len(topics))
    plan = []
    for index, topic in enumerate(topics[:7], start=1):
        if topic in missing:
            task = (f"Spend 30–45 minutes learning the fundamentals of {topic}. "
                    "Write a short note and complete one beginner exercise. "
                    "Only add it to your resume after you can demonstrate it.")
        else:
            task = (f"{topic}: review one project example, prepare a concise explanation, "
                    "and practice a related interview question.")
        plan.append({"day": f"Day {index}", "focus": topic, "task": task})
    return plan

def analyze(resume_text: str, job_description: str) -> Dict:
    resume, job = resume_text.strip(), job_description.strip()
    job_skills, resume_skills = detect_skills(job), detect_skills(resume)
    matched = [s for s in job_skills if s in resume_skills]
    missing = [s for s in job_skills if s not in resume_skills]
    coverage = len(matched) / len(job_skills) if job_skills else 0.0
    similarity = _similarity(resume, job)
    score = 0.55 * similarity + 0.45 * coverage
    evidence = {s: _evidence_for_skill(resume, s) for s in matched}
    return {
        "overall_score": round(score * 100),
        "text_similarity": round(similarity * 100),
        "skill_coverage": round(coverage * 100),
        "job_skill_count": len(job_skills),
        "job_skills": job_skills, "resume_skills": resume_skills,
        "matched_skills": matched, "missing_skills": missing,
        "evidence": evidence, "learning_plan": _learning_plan(missing),
    }

def extract_text(file_bytes: bytes, filename: str) -> str:
    suffix = filename.lower().rsplit(".", 1)[-1]
    if suffix == "txt":
        return file_bytes.decode("utf-8", errors="replace")
    if suffix == "pdf":
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(file_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if suffix == "docx":
        from docx import Document
        document = Document(io.BytesIO(file_bytes))
        return "\n".join(p.text for p in document.paragraphs)
    raise ValueError("Unsupported file type. Upload PDF, DOCX, or TXT.")
