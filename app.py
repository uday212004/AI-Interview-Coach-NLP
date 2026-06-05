"""
AI Interview Coach — Premium SaaS UI
Phase 12: Complete Design Overhaul
"""

import os
import streamlit as st

from src.parser import ResumeParser
from src.skill_extractor import SkillExtractor
from src.matcher import RoleMatcher
from src.question_generator import QuestionGenerator
from src.evaluator import AnswerEvaluator
from src.readiness import ReadinessEngine
from src.dashboard import Dashboard


# ─────────────────────────────────────────────────────────────
#  PAGE CONFIG  (must be the very first Streamlit call)
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ─────────────────────────────────────────────────────────────
#  INJECT CUSTOM CSS
# ─────────────────────────────────────────────────────────────
def load_css(path: str) -> None:
    """Inject a local CSS file into the Streamlit app."""
    with open(path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("assets/style.css")


# ─────────────────────────────────────────────────────────────
#  HELPER: Render an HTML block
# ─────────────────────────────────────────────────────────────
def html(markup: str) -> None:
    st.markdown(markup, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    html("""
    <div style="padding: 0 0.5rem 2rem;">
        <div style="
            font-family: 'Syne', sans-serif;
            font-size: 1.35rem;
            font-weight: 800;
            background: linear-gradient(135deg, #38BDF8, #8B5CF6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.03em;
            line-height: 1.2;
            margin-bottom: 0.25rem;
        ">AI Interview<br>Coach</div>
        <div style="
            font-size: 0.72rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: #475569;
        ">Premium SaaS Edition</div>
    </div>
    """)

    html("""
    <div style="
        background: linear-gradient(135deg, rgba(56,189,248,0.12), rgba(139,92,246,0.12));
        border: 1px solid rgba(56,189,248,0.20);
        border-radius: 14px;
        padding: 1rem;
        margin-bottom: 1.5rem;
    ">
        <div style="font-size: 0.75rem; color: #94A3B8; font-weight: 600;
                    text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.75rem;">
            WORKFLOW
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
    """)

    steps = [
        ("📄", "Upload Resume"),
        ("🔍", "Extract Skills"),
        ("🎯", "Match Role"),
        ("🎤", "Practice Questions"),
        ("📊", "View Analytics"),
    ]
    for icon, label in steps:
        html(f"""
        <div style="display:flex; align-items:center; gap:0.6rem;
                    font-size:0.82rem; color:#CBD5E1; font-weight:500;">
            <span style="font-size:1rem;">{icon}</span> {label}
        </div>
        """)

    html("</div></div>")

    html("""
    <div style="
        border-top: 1px solid rgba(56,189,248,0.12);
        padding-top: 1.25rem;
        margin-top: 0.5rem;
    ">
        <div style="font-size: 0.72rem; color: #475569; font-weight: 600;
                    text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.75rem;">
            ABOUT
        </div>
        <div style="font-size: 0.8rem; color: #64748B; line-height: 1.6;">
            Powered by <span style="color:#38BDF8; font-weight:600;">spaCy</span>,
            <span style="color:#8B5CF6; font-weight:600;">NLTK</span> &
            <span style="color:#10B981; font-weight:600;">Sentence Transformers</span>.
            Built for serious candidates.
        </div>
    </div>
    """)


# ─────────────────────────────────────────────────────────────
#  MAIN HEADER
# ─────────────────────────────────────────────────────────────
html("""
<div style="margin-bottom: 2rem;">
    <h1 style="margin-bottom: 0.2rem;">🎯 AI Interview Coach</h1>
    <p style="color: #64748B; font-size: 0.9rem; margin: 0; font-weight: 400;">
        Upload your resume and land your next role with AI-powered preparation.
    </p>
</div>
""")


# ─────────────────────────────────────────────────────────────
#  FILE UPLOAD SECTION
# ─────────────────────────────────────────────────────────────
html("""
<div class="section-banner">
    <span class="icon">📄</span>
    <div>
        <div class="label">Resume Upload</div>
        <div class="sublabel">PDF format · Max 10 MB · Parsed instantly</div>
    </div>
</div>
""")

uploaded_file = st.file_uploader(
    "Drop your resume here or click to browse",
    type=["pdf"],
    label_visibility="collapsed",
)


# ─────────────────────────────────────────────────────────────
#  EMPTY STATE
# ─────────────────────────────────────────────────────────────
if not uploaded_file:
    html("""
    <div class="hero-empty">
        <span class="hero-icon">🚀</span>
        <h2>Start Your Interview Journey</h2>
        <p>
            Upload your resume above and our AI engine will extract your skills,
            match you to your target role, generate interview questions, and
            evaluate your answers — all in one seamless workflow.
        </p>
        <div class="feature-grid">
            <div class="feature-item">
                <div class="f-icon">🔍</div>
                <div class="f-label">Skill Extraction</div>
            </div>
            <div class="feature-item">
                <div class="f-icon">📈</div>
                <div class="f-label">Role Matching</div>
            </div>
            <div class="feature-item">
                <div class="f-icon">🎤</div>
                <div class="f-label">Mock Interview</div>
            </div>
            <div class="feature-item">
                <div class="f-icon">✍️</div>
                <div class="f-label">Answer Eval</div>
            </div>
            <div class="feature-item">
                <div class="f-icon">🚀</div>
                <div class="f-label">Readiness Score</div>
            </div>
            <div class="feature-item">
                <div class="f-icon">📊</div>
                <div class="f-label">Analytics</div>
            </div>
        </div>
    </div>
    """)
    st.stop()


# ─────────────────────────────────────────────────────────────
#  SAVE RESUME
# ─────────────────────────────────────────────────────────────
os.makedirs("resumes", exist_ok=True)
save_path = f"resumes/{uploaded_file.name}"
with open(save_path, "wb") as f:
    f.write(uploaded_file.getbuffer())


# ═════════════════════════════════════════════════════════════
#  SECTION 1 — RESUME PARSING
# ═════════════════════════════════════════════════════════════
html("""
<div class="section-divider">
    <span class="divider-label">Resume Analysis</span>
</div>
<div class="section-banner">
    <span class="icon">🔍</span>
    <div>
        <div class="label">Parsed Resume</div>
        <div class="sublabel">Raw text extracted and ready for analysis</div>
    </div>
</div>
""")

with st.spinner("Parsing resume…"):
    parser = ResumeParser()
    text = parser.extract_text(save_path)

st.success("✅  Resume parsed successfully — text extracted and ready for skill analysis.")

with st.expander("📄  View Extracted Resume Text"):
    st.write(text)


# ═════════════════════════════════════════════════════════════
#  SECTION 2 — SKILL EXTRACTION
# ═════════════════════════════════════════════════════════════
html("""
<div class="section-banner" style="margin-top:1.5rem;">
    <span class="icon">🛠</span>
    <div>
        <div class="label">Extracted Skills</div>
        <div class="sublabel">NLP-detected technical & soft skills from your resume</div>
    </div>
</div>
""")

with st.spinner("Extracting skills…"):
    extractor = SkillExtractor()
    skills = extractor.extract_skills(text)
    frequency = extractor.skill_frequency(text)

if skills:
    # Render skills as badge chips
    badges_html = '<div class="badge-grid">'
    for skill in skills:
        badges_html += f'<span class="skill-badge neutral">✦ {skill.title()}</span>'
    badges_html += "</div>"
    html(badges_html)
else:
    st.warning("⚠️  No skills detected. Ensure your resume contains technical keywords.")


# ── Skill Frequency ──────────────────────────────────────────
if frequency:
    html("""
    <div style="margin-top: 1.5rem;">
        <h2>📊 Skill Frequency</h2>
    </div>
    """)

    with st.expander("📈  View Skill Frequency Data"):
        st.write(frequency)


# ═════════════════════════════════════════════════════════════
#  SECTION 3 — ROLE MATCHING
# ═════════════════════════════════════════════════════════════
html("""
<div class="section-divider">
    <span class="divider-label">Role Matching Engine</span>
</div>
<div class="section-banner">
    <span class="icon">🎯</span>
    <div>
        <div class="label">Target Role</div>
        <div class="sublabel">Select the role you are interviewing for</div>
    </div>
</div>
""")

col_role, col_spacer = st.columns([1, 1])
with col_role:
    role = st.selectbox(
        "Target Role",
        [
            "Data Analyst",
            "Business Analyst",
            "Data Scientist",
            "ML Engineer",
            "Data Engineer",
            "AI Engineer",
        ],
        label_visibility="collapsed",
    )

with st.spinner("Calculating match score…"):
    matcher = RoleMatcher()
    result = matcher.calculate_match(skills, role)

# KPI Row
html("<h2>📈 Role Match Score</h2>")
k1, k2, k3 = st.columns(3)
k1.metric("Match Score", f"{result['score']}%")
k2.metric("Matched Skills", len(result["matched"]))
k3.metric("Missing Skills", len(result["missing"]))

# Matched Skills
if result["matched"]:
    html("<h2>✅ Matched Skills</h2>")
    matched_html = '<div class="badge-grid">'
    for skill in result["matched"]:
        matched_html += f'<span class="skill-badge matched">✓ {skill.title()}</span>'
    matched_html += "</div>"
    html(matched_html)

# Missing Skills
if result["missing"]:
    html('<div style="margin-top: 1rem;"><h2>❌ Missing Skills</h2></div>')
    missing_html = '<div class="badge-grid">'
    for skill in result["missing"]:
        missing_html += f'<span class="skill-badge missing">✕ {skill.title()}</span>'
    missing_html += "</div>"
    html(missing_html)

# Career Insight
insight_text = matcher.generate_insight(result["score"])
html(f"""
<div style="margin-top: 1.25rem;">
    <h2>💡 Career Insight</h2>
    <div class="insight-box">
        <span class="insight-icon">🧠</span>{insight_text}
    </div>
</div>
""")


# ═════════════════════════════════════════════════════════════
#  SECTION 4 — QUESTION GENERATOR
# ═════════════════════════════════════════════════════════════
html("""
<div class="section-divider">
    <span class="divider-label">Interview Practice</span>
</div>
<div class="section-banner">
    <span class="icon">🎤</span>
    <div>
        <div class="label">Interview Question Generator</div>
        <div class="sublabel">Curated questions based on your target role and difficulty</div>
    </div>
</div>
""")

col_diff, col_cat = st.columns(2)
with col_diff:
    html('<div class="upload-label">Difficulty Level</div>')
    difficulty = st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard"],
        label_visibility="collapsed",
    )

with col_cat:
    html('<div class="upload-label">Question Category</div>')
    category = st.selectbox(
        "Category",
        ["Technical", "Behavioral", "Scenario-Based"],
        label_visibility="collapsed",
    )

with st.spinner("Generating questions…"):
    generator = QuestionGenerator()
    questions = generator.get_questions(role, difficulty, category)

if questions:
    html(f"<h2>📋 Generated Questions <span style='color:#475569; font-size:0.8rem; font-weight:500;'>({len(questions)} total)</span></h2>")
    for i, question in enumerate(questions, start=1):
        html(f"""
        <div class="question-card">
            <span class="q-num">Q{i:02d}</span>
            <span class="q-text">{question}</span>
        </div>
        """)
else:
    st.warning("⚠️  No questions found for the selected combination. Try different filters.")


# ═════════════════════════════════════════════════════════════
#  SECTION 5 — ANSWER EVALUATION
# ═════════════════════════════════════════════════════════════
if questions:
    html("""
    <div class="section-divider">
        <span class="divider-label">Answer Evaluation</span>
    </div>
    <div class="section-banner">
        <span class="icon">✍️</span>
        <div>
            <div class="label">Evaluate Your Answer</div>
            <div class="sublabel">Select a question, write your answer, and receive AI feedback</div>
        </div>
    </div>
    """)

    html('<div class="upload-label">Select a Question to Answer</div>')
    selected_question = st.selectbox(
        "Select Question",
        questions,
        label_visibility="collapsed",
    )

    html("""
    <div style="margin: 0.75rem 0 0.35rem;">
        <div class="upload-label">Your Answer</div>
    </div>
    """)
    user_answer = st.text_area(
        "Write Your Answer",
        height=200,
        placeholder="Write a clear, structured answer here. Use the STAR method for behavioral questions: Situation → Task → Action → Result.",
        label_visibility="collapsed",
    )

    st.button("🚀  Evaluate My Answer", type="primary")

    if st.session_state.get("FormSubmitter:Form-Evaluate My Answer") or True:
        # We check the button directly via session state key trick;
        # fall through only when button is actually clicked
        pass

    evaluate_clicked = st.button(
        "Evaluate Answer",
        key="evaluate_btn",
        help="Click to get AI-powered feedback on your answer",
    )

    # Remove the duplicate button above; use only evaluate_clicked
    if evaluate_clicked:
        if user_answer.strip() == "":
            st.warning("⚠️  Please enter an answer before evaluating.")
        else:
            with st.spinner("Evaluating your answer with AI…"):
                evaluator = AnswerEvaluator()
                evaluation = evaluator.evaluate_answer(selected_question, user_answer)

            # ── Score KPIs ───────────────────────────────────────
            html("""
            <div class="section-divider">
                <span class="divider-label">Evaluation Results</span>
            </div>
            <h2>📊 Evaluation Scores</h2>
            """)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Overall Score",    f"{evaluation['score']}%")
            c2.metric("Technical",        f"{evaluation['technical_score']}%")
            c3.metric("Communication",    f"{evaluation['communication_score']}%")
            c4.metric("Completeness",     f"{evaluation['completeness_score']}%")

            # ── Ideal Answer ─────────────────────────────────────
            html("""
            <div style="margin-top: 1.5rem;">
                <h2>🎯 Ideal Answer</h2>
            </div>
            """)
            html(f"""
            <div class="insight-box">
                <span class="insight-icon">💡</span>{evaluation["ideal_answer"]}
            </div>
            """)

            # ── Strengths / Weaknesses / Suggestions (3 cols) ───
            html("<div style='margin-top: 1.5rem;'>")
            col_s, col_w, col_sg = st.columns(3)

            with col_s:
                html("""
                <div class="eval-panel">
                    <div class="panel-title">✅ Strengths</div>
                """)
                for item in evaluation["strengths"]:
                    html(f'<div class="eval-item strength">✦ {item}</div>')
                html("</div>")

            with col_w:
                html("""
                <div class="eval-panel">
                    <div class="panel-title">❌ Weaknesses</div>
                """)
                for item in evaluation["weaknesses"]:
                    html(f'<div class="eval-item weakness">✕ {item}</div>')
                html("</div>")

            with col_sg:
                html("""
                <div class="eval-panel">
                    <div class="panel-title">💡 Suggestions</div>
                """)
                for item in evaluation["suggestions"]:
                    html(f'<div class="eval-item suggestion">→ {item}</div>')
                html("</div>")

            html("</div>")

            # ═══════════════════════════════════════════════════
            #  SECTION 6 — READINESS ENGINE
            # ═══════════════════════════════════════════════════
            with st.spinner("Computing interview readiness…"):
                readiness_engine = ReadinessEngine()
                readiness = readiness_engine.calculate_readiness(
                    role_match_score=result["score"],
                    answer_score=evaluation["score"],
                    extracted_skills=skills,
                    missing_skills=result["missing"],
                )

            html("""
            <div class="section-divider">
                <span class="divider-label">Interview Readiness</span>
            </div>
            <div class="section-banner">
                <span class="icon">🚀</span>
                <div>
                    <div class="label">Readiness Assessment</div>
                    <div class="sublabel">How prepared are you for the interview today?</div>
                </div>
            </div>
            """)

            r1, r2, r3 = st.columns(3)
            r1.metric("Readiness Score", f"{readiness['readiness_score']}%")
            r2.metric("Skill Coverage",  f"{readiness['skill_coverage']}%")
            r3.metric("Level",           readiness["level"])

            # Readiness level badge
            level_lower = readiness["level"].lower()
            badge_class = (
                "advanced"     if level_lower == "advanced"     else
                "intermediate" if level_lower == "intermediate" else
                "beginner"
            )
            html(f"""
            <div style="display:flex; align-items:center; gap:1rem; margin-top:1rem;">
                <span class="readiness-badge {badge_class}">
                    {"🏆" if badge_class == "advanced" else "🔥" if badge_class == "intermediate" else "🌱"}
                    {readiness["level"]}
                </span>
                <div class="insight-box" style="flex:1; margin:0;">
                    {readiness["insight"]}
                </div>
            </div>
            """)

            # ═══════════════════════════════════════════════════
            #  SECTION 7 — ANALYTICS DASHBOARD
            # ═══════════════════════════════════════════════════
            html("""
            <div class="section-divider">
                <span class="divider-label">Analytics Dashboard</span>
            </div>
            <div class="section-banner">
                <span class="icon">📊</span>
                <div>
                    <div class="label">Performance Analytics</div>
                    <div class="sublabel">Visual breakdown of your interview readiness metrics</div>
                </div>
            </div>
            """)

            dashboard = Dashboard()

            # Top KPI strip
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Role Match",    f"{result['score']}%")
            k2.metric("Answer Score",  f"{evaluation['score']}%")
            k3.metric("Readiness",     f"{readiness['readiness_score']}%")
            k4.metric("Skills Found",  len(skills))

            # Row 1 — Gauges
            html("<h2 style='margin-top:1.5rem;'>🔵 Score Gauges</h2>")
            g1, g2 = st.columns(2)
            with g1:
                st.plotly_chart(
                    dashboard.match_score_gauge(result["score"]),
                    use_container_width=True,
                )
            with g2:
                st.plotly_chart(
                    dashboard.readiness_gauge(readiness["readiness_score"]),
                    use_container_width=True,
                )

            # Row 2 — Distribution & Gap
            html("<h2>🟣 Skill Analytics</h2>")
            d1, d2 = st.columns(2)
            with d1:
                st.plotly_chart(
                    dashboard.skill_distribution(frequency),
                    use_container_width=True,
                )
            with d2:
                st.plotly_chart(
                    dashboard.skill_gap_chart(result["matched"], result["missing"]),
                    use_container_width=True,
                )

            # Row 3 — Radar
            html("<h2>🕸 Competency Radar</h2>")
            st.plotly_chart(
                dashboard.radar_chart(
                    evaluation["technical_score"],
                    evaluation["communication_score"],
                    evaluation["completeness_score"],
                    readiness["readiness_score"],
                ),
                use_container_width=True,
            )

            # Footer note
            html("""
            <div style="
                margin-top: 3rem;
                text-align: center;
                color: #334155;
                font-size: 0.78rem;
                font-weight: 500;
                letter-spacing: 0.04em;
            ">
                AI Interview Coach · Premium SaaS Edition · Powered by spaCy, NLTK & Sentence Transformers
            </div>
            """)
