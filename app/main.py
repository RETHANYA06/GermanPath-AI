import streamlit as st

from app.data.content_loader import load_vocabulary_topics
from app.quizzes.quiz_engine import generate_question

st.set_page_config(
    page_title="GermanPath AI",
    page_icon="🇩🇪",
    layout="wide"
)

st.sidebar.title("🇩🇪 GermanPath AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Vocabulary",
        "Flashcards",
        "Quick Quiz",
        "Practice Test",
        "Mock Exam",
        "Progress"
    ]
)

# HOME PAGE
if page == "Home":

    st.title("🇩🇪 GermanPath AI")

    st.markdown("""
    Learn German from A1 to B1 for free.

    Features:
    - Vocabulary Learning
    - Example Sentences
    - Quizzes
    - Progress Tracking
    - Goethe Exam Preparation
    """)

# VOCABULARY PAGE
elif page == "Vocabulary":

    st.title("📚 A1 Vocabulary")

    words = load_vocabulary_topics()

    st.metric("Total A1 Words", len(words))

    for word in words:
        st.success(
            f"{word['german']} → {word['english']}"
        )

elif page == "Flashcards":

    from app.flashcards.flashcard_engine import get_flashcard

    st.title("🃏 Flashcards")

    if "flashcard" not in st.session_state:
        st.session_state.flashcard = get_flashcard()

    card = st.session_state.flashcard

    st.subheader(card["german"])

    if st.button("Show Meaning"):
        st.success(card["english"])

    if st.button("Next Flashcard"):
        st.session_state.flashcard = get_flashcard()
        st.rerun()

# QUIZ PAGE
elif page == "Quiz":

    QUIZ_TYPES = {
    "Quick Quiz": 10,
    "Practice Test": 25,
    "Mock Exam": 50
}

    st.title("📝 German Quiz")

    if "score" not in st.session_state:
        st.session_state["score"] = 0

    if "questions_answered" not in st.session_state:
        st.session_state["questions_answered"] = 0

    if "question" not in st.session_state:
        st.session_state["question"] = generate_question()

    question = st.session_state["question"]

    st.metric(
        "Score",
        f"{st.session_state['score']}/{st.session_state['questions_answered']}"
    )
    st.session_state.total_questions = 10
    st.session_state.current_question = 1

    if st.session_state["questions_answered"] > 0:

        accuracy = (
            st.session_state["score"]
            / st.session_state["questions_answered"]
        ) * 100

        st.metric(
            "Accuracy",
            f"{accuracy:.1f}%"
        )

    st.caption(
        f"Topic: {question['topic']}"
    )

    st.subheader(
        f"What is the meaning of '{question['word']}'?"
    )

    answer = st.radio(
        "Choose an answer",
        question["options"]
    )

    if st.button("Check Answer"):

        st.session_state["questions_answered"] += 1

        if answer == question["correct"]:

            st.session_state["score"] += 1

            st.success("✅ Correct!")

        else:

            st.error(
                f"❌ Wrong! Correct answer: {question['correct']}"
            )

    if st.button("Next Question"):

        st.session_state["question"] = generate_question()

        st.rerun()

# PROGRESS PAGE
elif page == "Progress":

    words = load_vocabulary_topics()

    st.title("🎯 Progress Tracker")

    st.progress(25)

    st.metric(
        "Vocabulary Database",
        f"{len(words)} Words"
    )

    st.metric(
        "Current Level",
        "A1"
    )

    st.metric(
        "Topics Completed",
        "10"
    )

elif page == "Quick Quiz":

    st.title("⚡ Quick Quiz")

    st.write("10 Questions")

    st.info("Coming Soon")


elif page == "Practice Test":

    st.title("📘 Practice Test")

    st.write("25 Questions")

    st.info("Coming Soon")


elif page == "Mock Exam":

    st.title("🎓 Mock Exam")

    st.write("50 Questions")

    st.info("Coming Soon")