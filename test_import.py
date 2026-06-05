

from sentence_transformers import SentenceTransformer

print("Installed Successfully")

import streamlit as st

from src.question_generator import QuestionGenerator

from src.evaluator import AnswerEvaluator

from src.parser import ResumeParser
from src.skill_extractor import SkillExtractor
from src.matcher import RoleMatcher

from src.readiness import ReadinessEngine



# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="AI Interview Coach",
    layout="wide"
)

st.title("🎯 AI Interview Coach")

# -----------------------------------
# FILE UPLOAD
# -----------------------------------

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

# -----------------------------------
# PROCESS RESUME
# -----------------------------------

if uploaded_file:

    save_path = f"resumes/{uploaded_file.name}"

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Parse Resume
    parser = ResumeParser()

    text = parser.extract_text(save_path)

    st.success("✅ Resume Parsed Successfully")

    # Show Resume Text
    with st.expander("View Resume Text"):
        st.write(text)

    # -----------------------------------
    # SKILL EXTRACTION
    # -----------------------------------

    extractor = SkillExtractor()

    skills = extractor.extract_skills(text)

    frequency = extractor.skill_frequency(text)

    st.subheader("🛠 Extracted Skills")

    if skills:

        cols = st.columns(4)

        for i, skill in enumerate(skills):
            cols[i % 4].success(skill.title())

    else:
        st.warning("No skills found.")

    # -----------------------------------
    # SKILL FREQUENCY
    # -----------------------------------

    st.subheader("📊 Skill Frequency")

    if frequency:
        st.write(frequency)

    else:
        st.warning("No skill frequency data available.")

    # -----------------------------------
    # ROLE MATCHING ENGINE
    # -----------------------------------

    st.subheader("🎯 Target Role")

    role = st.selectbox(
        "Select Your Target Role",
        [
            "Data Analyst",
            "Business Analyst",
            "Data Scientist",
            "ML Engineer",
            "Data Engineer",
            "AI Engineer"
        ]
    )

    matcher = RoleMatcher()

    result = matcher.calculate_match(
        skills,
        role
    )

    st.subheader("📈 Role Match Score")

    st.metric(
        "Match Score",
        f"{result['score']}%"
    )

    # Matched Skills

    st.subheader("✅ Matched Skills")

    if result["matched"]:

        cols = st.columns(3)

        for i, skill in enumerate(result["matched"]):
            cols[i % 3].success(skill.title())

    # Missing Skills

    st.subheader("❌ Missing Skills")

    if result["missing"]:

        cols = st.columns(3)

        for i, skill in enumerate(result["missing"]):
            cols[i % 3].error(skill.title())

    # Career Insight

    insight = matcher.generate_insight(
        result["score"]
    )

    st.subheader("💡 Career Insight")

    st.info(insight)

# -----------------------------------
# INTERVIEW QUESTION GENERATOR
# -----------------------------------

    
    st.subheader("🎤 Interview Question Generator")

    difficulty = st.selectbox(
        "Select Difficulty",
        [
            "Easy",
            "Medium",
            "Hard"
        ]
    )

    category = st.selectbox(
        "Select Category",
        [
            "Technical",
            "Behavioral",
            "Scenario-Based"
        ]
    )

    generator = QuestionGenerator()

    questions = generator.get_questions(
        role,
        difficulty,
        category
    )

    if questions:

        st.subheader("📋 Generated Questions")

        for i, question in enumerate(
            questions,
            start=1
        ):

            st.info(
                f"{i}. {question}"
            )

    else:

        st.warning(
            "No questions found for this selection."
        )






# -----------------------------------
# ANSWER EVALUATION ENGINE
# -----------------------------------



    st.subheader("✍ Answer Evaluation")

    selected_question = st.selectbox(
        "Select Question",
        questions
    )

    user_answer = st.text_area(
        "Write Your Answer",
        height=200
    )

    if st.button("Evaluate Answer"):

        if user_answer.strip() == "":

            st.warning(
                "Please enter an answer."
            )

        else:

            evaluator = AnswerEvaluator()

            evaluation = (
                evaluator.evaluate_answer(
                    selected_question,
                    user_answer
                )
            )


            readiness_engine = ReadinessEngine()
            readiness = (
                readiness_engine.calculate_readiness(
                    role_match_score=result["score"],
                    answer_score=evaluation["score"],
                    extracted_skills=result["matched"],
                    missing_skills=result["missing"]
                )
            )

            
            

            st.subheader(
                "📊 Evaluation Results"
            )

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Overall Score",
                f"{evaluation['score']}%"
            )

            col2.metric(
                "Technical",
                f"{evaluation['technical_score']}%"
            )

            col3.metric(
                "Communication",
                f"{evaluation['communication_score']}%"
            )

            col4.metric(
                "Completeness",
                f"{evaluation['completeness_score']}%"
            )

            st.subheader(
                "🎯 Ideal Answer"
            )

            st.info(
                evaluation["ideal_answer"]
            )

            st.subheader(
                "✅ Strengths"
            )

            for item in evaluation["strengths"]:
                st.success(item)

            st.subheader(
                "❌ Weaknesses"
            )

            for item in evaluation["weaknesses"]:
                st.error(item)

            st.subheader(
                "💡 Suggestions"
            )

            for item in evaluation["suggestions"]:
                st.warning(item)


            st.subheader(
    "🚀 Interview Readiness"
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Readiness Score",
    f"{readiness['readiness_score']}%"
)

col2.metric(
    "Skill Coverage",
    f"{readiness['skill_coverage']}%"
)

col3.metric(
    "Level",
    readiness["level"]
)

st.success(
    readiness["insight"]
)
    
