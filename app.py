import streamlit as st
from analyzer import analyze, extract_text

st.set_page_config(page_title="ProofMatch AI", page_icon="🧭", layout="wide")
st.title("🧭 ProofMatch AI")
st.subheader("Evidence-first job readiness analyzer")
st.write("Compare your resume with a job description, inspect evidence behind matching skills, and turn gaps into a focused learning plan.")

with st.sidebar:
    st.header("How it works")
    st.write("1. Add your resume.\n2. Paste a job description.\n3. Review matches, evidence, and skill gaps.")
    st.caption("Analysis runs locally. No external AI API is used.")
    st.info("The match indicator is an educational heuristic, not a hiring prediction or official ATS score.")

resume_tab, job_tab = st.tabs(["📄 Resume", "🎯 Job description"])
with resume_tab:
    uploaded = st.file_uploader("Upload a resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
    pasted = st.text_area("Or paste resume text", height=260)
with job_tab:
    job = st.text_area("Paste the complete job description", height=320)

resume = pasted.strip()
if uploaded is not None:
    try:
        extracted = extract_text(uploaded.getvalue(), uploaded.name)
        if extracted.strip():
            resume = extracted.strip()
            st.success(f"Read {uploaded.name}")
        else:
            st.warning("No selectable text found. Try a text-based PDF or paste the resume text.")
    except Exception as exc:
        st.error(f"Could not read this file: {exc}")

if st.button("Analyze my match", type="primary", use_container_width=True):
    if len(resume) < 40:
        st.error("Please provide at least 40 characters of resume text.")
    elif len(job.strip()) < 40:
        st.error("Please paste a job description of at least 40 characters.")
    else:
        st.session_state["analysis"] = analyze(resume, job)

result = st.session_state.get("analysis")
if result:
    st.divider()
    st.header("Your match snapshot")
    c1, c2, c3 = st.columns(3)
    c1.metric("Guidance score", f"{result['overall_score']}%")
    c2.metric("Job skills found", f"{len(result['matched_skills'])}/{result['job_skill_count']}")
    c3.metric("Skills to investigate", len(result["missing_skills"]))
    st.progress(result["overall_score"] / 100)
    st.caption(f"Text similarity: {result['text_similarity']}% · Skill coverage: {result['skill_coverage']}%")

    left, right = st.columns(2)
    with left:
        st.subheader("✅ Skills with resume evidence")
        if result["matched_skills"]:
            for skill in result["matched_skills"]:
                with st.expander(skill):
                    for sentence in result["evidence"].get(skill, []):
                        st.write(f"“{sentence}”")
        else:
            st.write("No skills from the current vocabulary were detected in both texts.")
    with right:
        st.subheader("🔎 Skills not found in resume")
        if result["missing_skills"]:
            for skill in result["missing_skills"]:
                st.write(f"• {skill}")
        else:
            st.success("All detected job-description skills also appear in the resume.")
        st.caption("Not found means absent from the supplied text, not necessarily absent from your abilities.")

    st.subheader("🗓️ Your seven-day improvement plan")
    for day in result["learning_plan"]:
        st.markdown(f"**{day['day']} — {day['focus']}**")
        st.write(day["task"])

    report = ["# ProofMatch AI — Analysis Report", "", f"- Guidance score: {result['overall_score']}%", f"- Text similarity: {result['text_similarity']}%", f"- Skill coverage: {result['skill_coverage']}%", "", "## Skills with evidence"]
    report += [f"- {s}: {' | '.join(result['evidence'].get(s, []))}" for s in result["matched_skills"]]
    report += ["", "## Skills not found in resume text"] + [f"- {s}" for s in result["missing_skills"]]
    report += ["", "## Seven-day plan"] + [f"- {d['day']} — {d['focus']}: {d['task']}" for d in result["learning_plan"]]
    report += ["", "Note: educational heuristic, not a hiring prediction."]
    st.download_button("Download analysis report", data="\n".join(report), file_name="proofmatch-analysis.md", mime="text/markdown")
