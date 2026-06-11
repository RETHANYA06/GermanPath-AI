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
        "Reading",
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

elif page == "Reading":

    from app.reading.reading_engine import get_random_reading

    st.title("📖 Reading Practice")

    if "reading" not in st.session_state:
        st.session_state.reading = get_random_reading()

    reading = st.session_state.reading

    st.subheader(reading["title"])

    st.write(reading["passage"])

    st.markdown("---")

    st.write(reading["question"])

    answer = st.radio(
        "Choose an answer",
        reading["options"]
    )

    if st.button("Check Reading Answer"):

        if answer == reading["answer"]:

            st.success("✅ Correct")

        else:

            st.error(
                f"❌ Correct answer: {reading['answer']}"
            )

    if st.button("Next Reading"):

        st.session_state.reading = get_random_reading()

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

    TOTAL_QUESTIONS = 10

    if "quick_quiz" not in st.session_state:

        st.session_state.quick_quiz = {
            "current": 1,
            "total": TOTAL_QUESTIONS,
            "score": 0,
            "question": generate_question(),
            "answered": False
        }

    quiz = st.session_state.quick_quiz

    if quiz["current"] > quiz["total"]:

        accuracy = (
            quiz["score"] / quiz["total"]
        ) * 100

        st.success("🎉 Quiz Completed!")

        st.metric(
            "Final Score",
            f"{quiz['score']}/{quiz['total']}"
        )

        st.metric(
            "Accuracy",
            f"{accuracy:.1f}%"
        )

        if st.button("Restart Quiz"):

            del st.session_state.quick_quiz

            st.rerun()

    else:

        st.progress(
            quiz["current"] / quiz["total"]
        )

        st.write(
            f"Question {quiz['current']} / {quiz['total']}"
        )

        st.write(
            f"Score: {quiz['score']}"
        )

        question = quiz["question"]

        st.caption(
            f"Topic: {question['topic']}"
        )

        st.subheader(
            question["word"]
        )

        answer = st.radio(
            "Choose an answer",
            question["options"],
            key=f"qq_{quiz['current']}"
        )

        if not quiz["answered"]:

            if st.button("Check Answer"):

                quiz["answered"] = True

                if answer == question["correct"]:

                    quiz["score"] += 1

                    st.success("✅ Correct!")

                else:

                    st.error(
                        f"❌ Correct: {question['correct']}"
                    )

        else:

            if st.button("Next Question"):

                quiz["current"] += 1

                quiz["question"] = generate_question()

                quiz["answered"] = False

                st.rerun()


elif page == "Practice Test":

    st.title("📘 Practice Test")

    TOTAL_QUESTIONS = 25

    if "practice_test" not in st.session_state:

        st.session_state.practice_test = {
            "current": 1,
            "total": TOTAL_QUESTIONS,
            "score": 0,
            "question": generate_question(),
            "answered": False
        }

    quiz = st.session_state.practice_test

    if quiz["current"] > quiz["total"]:

        accuracy = (
            quiz["score"] / quiz["total"]
        ) * 100

        st.success("🎉 Practice Test Completed!")

        st.metric(
            "Final Score",
            f"{quiz['score']}/{quiz['total']}"
        )

        st.metric(
            "Accuracy",
            f"{accuracy:.1f}%"
        )

        if st.button("Restart Practice Test"):

            del st.session_state.practice_test

            st.rerun()

    else:

        st.progress(
            quiz["current"] / quiz["total"]
        )

        st.write(
            f"Question {quiz['current']} / {quiz['total']}"
        )

        st.write(
            f"Score: {quiz['score']}"
        )

        question = quiz["question"]

        st.caption(
            f"Topic: {question['topic']}"
        )

        st.subheader(
            question["word"]
        )

        answer = st.radio(
            "Choose an answer",
            question["options"],
            key=f"practice_{quiz['current']}"
        )

        if not quiz["answered"]:

            if st.button("Check Answer", key="practice_check"):

                quiz["answered"] = True

                if answer == question["correct"]:

                    quiz["score"] += 1

                    st.success("✅ Correct!")

                else:

                    st.error(
                        f"❌ Correct: {question['correct']}"
                    )

        else:

            if st.button("Next Question", key="practice_next"):

                quiz["current"] += 1

                quiz["question"] = generate_question()

                quiz["answered"] = False

                st.rerun()


elif page == "Mock Exam":

    st.title("🎓 Mock Exam")

    TOTAL_QUESTIONS = 50

    if "mock_exam" not in st.session_state:

        st.session_state.mock_exam = {
            "current": 1,
            "total": TOTAL_QUESTIONS,
            "score": 0,
            "question": generate_question(),
            "answered": False
        }

    quiz = st.session_state.mock_exam

    if quiz["current"] > quiz["total"]:

        accuracy = (
            quiz["score"] / quiz["total"]
        ) * 100

        st.success("🎉 Mock Exam Completed!")

        st.metric(
            "Final Score",
            f"{quiz['score']}/{quiz['total']}"
        )

        st.metric(
            "Accuracy",
            f"{accuracy:.1f}%"
        )

        if st.button("Restart Mock Exam"):

            del st.session_state.mock_exam

            st.rerun()

    else:

        st.progress(
            quiz["current"] / quiz["total"]
        )

        st.write(
            f"Question {quiz['current']} / {quiz['total']}"
        )

        st.write(
            f"Score: {quiz['score']}"
        )

        question = quiz["question"]

        st.caption(
            f"Topic: {question['topic']}"
        )

        st.subheader(
            question["word"]
        )

        answer = st.radio(
            "Choose an answer",
            question["options"],
            key=f"mock_{quiz['current']}"
        )

        if not quiz["answered"]:

            if st.button("Check Answer", key="mock_check"):

                quiz["answered"] = True

                if answer == question["correct"]:

                    quiz["score"] += 1

                    st.success("✅ Correct!")

                else:

                    st.error(
                        f"❌ Correct: {question['correct']}"
                    )

        else:

            if st.button("Next Question", key="mock_next"):

                quiz["current"] += 1

                quiz["question"] = generate_question()

                quiz["answered"] = False

                st.rerun()