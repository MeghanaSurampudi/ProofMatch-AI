# ProofMatch AI — Evidence-First Job Readiness Analyzer

**Turn a job description into an evidence-backed skill gap plan.**

ProofMatch is a local, privacy-first NLP project that compares a resume with a job description. It shows job skills, resume skills, missing/not-yet-evidenced skills, resume sentences supporting matches, and a practical seven-day learning plan.

## Why it is different
Basic resume matchers often return only a score or keyword count. ProofMatch maps each matched skill to resume evidence so users can inspect why it matched. A missing skill means **not found in the supplied resume text**, not necessarily that the candidate does not possess it.

## Tech stack
Python · Streamlit · scikit-learn (TF-IDF and cosine similarity) · PyPDF · python-docx · regular expressions

## Run locally
Python 3.10 or newer is recommended.

```bash
git clone https://github.com/MeghanaSurampudi/ProofMatch-AI.git
cd ProofMatch-AI
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit, usually http://localhost:8501.

## Use it
1. Paste resume text or upload a PDF, DOCX, or TXT resume.
2. Paste the target job description.
3. Select **Analyze my match**.
4. Review the guidance score, skill coverage, evidence, gaps, and seven-day plan.
5. Download the Markdown report.

Sample text is available in `examples/`.

## How it works
1. Extract text from the supplied resume.
2. Detect skills using a transparent vocabulary and aliases.
3. Compare resume and job-description text with TF-IDF word/bigram features and cosine similarity.
4. Calculate skill coverage.
5. Blend text similarity (55%) and skill coverage (45%) into a guidance indicator.
6. Map matched skills to sentences from the resume.
7. Generate a rule-based learning plan for gaps.

**Important:** The score is a heuristic, not a hiring probability, validated prediction, or official ATS score. TF-IDF is lexical similarity, not a transformer embedding or generative AI model. Skill detection is limited by the included vocabulary and can miss synonyms and context.

## Privacy
Analysis runs locally in the Streamlit process. The app does not call an external AI API or intentionally store uploaded resumes. Do not deploy publicly with real personal resumes without adding authentication, secure hosting, retention controls, and a privacy notice.

## Limitations
- Scanned/image-only PDFs may not yield extractable text.
- The skill vocabulary is limited and should be expanded.
- A skill mention is not proof of proficiency.
- The plan is a rule-based starting point, not expert career advice.

## Future improvements
Richer skill taxonomy, labelled evaluation dataset, optional semantic embeddings, multilingual extraction, and automated tests.

Educational portfolio project demonstrating practical NLP, text processing, explainability, and responsible document handling.
