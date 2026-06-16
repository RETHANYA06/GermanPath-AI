import streamlit as st

from app.data.content_loader import load_vocabulary_topics
from app.quizzes.quiz_engine import generate_question
from app.data.stats import initialize_stats
from app.reading.reading_engine import get_random_reading
from app.data.progress_manager import (
    load_progress,
    save_progress
)

st.set_page_config(
    page_title="GermanPath AI",
    page_icon="🇩🇪",
    layout="wide"
)

if "stats" not in st.session_state:
    st.session_state.stats = load_progress()

st.sidebar.title("🇩🇪 GermanPath AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Vocabulary",
        "Grammar",
        "Flashcards",
        "Quick Quiz",
        "Practice Test",
        "Mock Exam",
        "Grammar Quiz",
        "Reading",
        "Progress"
    ]
)
if page == "Home":

    st.title("🇩🇪 GermanPath AI")

    st.markdown("""
    Learn German from A1 to B1 for free.

    ### Features

    - Vocabulary Learning
    - Flashcards
    - Quick Quiz
    - Practice Test
    - Mock Exam
    - Reading Practice
    - Progress Tracking
    - Goethe Exam Preparation
    """)
elif page == "Vocabulary":

    st.title("📚 A1 Vocabulary")

    words = load_vocabulary_topics()

    st.metric(
        "Total A1 Words",
        len(words)
    )

    search = st.text_input(
        "Search Vocabulary"
    )

    for word in words:

        if (
            search == ""
            or search.lower() in word["german"].lower()
            or search.lower() in word["english"].lower()
        ):

            st.success(
                f"{word['german']} → {word['english']}"
            )


elif page == "Grammar":

    from app.grammar.grammar_loader import (
        load_grammar_topics,
        load_grammar_content
    )

    st.title("🇩🇪 German Grammar")

    topics = load_grammar_topics()

    selected_topic = st.selectbox(
        "Choose Grammar Topic",
        topics
    )

    content = load_grammar_content(
        selected_topic
    )

    st.markdown(content)
    
elif page == "Flashcards":

    st.title("🃏 Flashcards")

    if "flashcard" not in st.session_state:

        st.session_state.flashcard = get_flashcard()

    card = st.session_state.flashcard

    st.subheader(
        card["german"]
    )

    if st.button("Show Meaning"):

        st.success(
            card["english"]
        )

    if st.button("Next Flashcard"):

        st.session_state.flashcard = get_flashcard()

        st.rerun()
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
            quiz["score"]
            / quiz["total"]
        ) * 100

        st.success("🎉 Quick Quiz Completed!")

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
            quiz["current"]
            / quiz["total"]
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
            key=f"quick_{quiz['current']}"
        )

        if not quiz["answered"]:

            if st.button("Check Answer"):

                quiz["answered"] = True

                st.session_state.stats["quiz_total"] += 1
                save_progress(
                     st.session_state.stats
                )
                if answer == question["correct"]:

                    quiz["score"] += 1

                    st.session_state.stats["quiz_correct"] += 1
                    save_progress(
                         st.session_state.stats
                    )

                    st.success("✅ Correct!")

                else:

                    st.error(
                        f"❌ Correct Answer: {question['correct']}"
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

    st.write(f"Question {quiz['current']} / {quiz['total']}")
    st.write(f"Score: {quiz['score']}")

    question = quiz["question"]

    st.subheader(question["word"])

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
                    f"❌ Correct Answer: {question['correct']}"
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
            quiz["score"]
            / quiz["total"]
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
            quiz["current"]
            / quiz["total"]
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

                st.session_state.stats["quiz_total"] += 1
                save_progress(
    st.session_state.stats
)

                if answer == question["correct"]:

                    quiz["score"] += 1

                    st.session_state.stats["quiz_correct"] += 1
                    save_progress(
    st.session_state.stats
)

                    st.success("✅ Correct!")

                else:

                    st.error(
                        f"❌ Correct Answer: {question['correct']}"
                    )

        else:

            if st.button("Next Question", key="mock_next"):

                quiz["current"] += 1

                quiz["question"] = generate_question()

                quiz["answered"] = False

                st.rerun()

elif page == "Reading":

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

        st.session_state.stats["reading_total"] += 1
        save_progress(
    st.session_state.stats
)

        if answer == reading["answer"]:

            st.session_state.stats["reading_correct"] += 1
            save_progress(
    st.session_state.stats
)

            st.success("✅ Correct!")

        else:

            st.error(
                f"❌ Correct Answer: {reading['answer']}"
            )

    if st.button("Next Reading"):

        st.session_state.reading = get_random_reading()

        st.rerun()

elif page == "Progress":

    st.title("📊 Progress Dashboard")

    stats = st.session_state.stats

    st.subheader("Quiz Statistics")

    st.metric(
        "Questions Attempted",
        stats["quiz_total"]
    )

    st.metric(
        "Correct Answers",
        stats["quiz_correct"]
    )

    if stats["quiz_total"] > 0:

        quiz_accuracy = (
            stats["quiz_correct"]
            / stats["quiz_total"]
        ) * 100

        st.metric(
            "Quiz Accuracy",
            f"{quiz_accuracy:.1f}%"
        )

    st.markdown("---")

    st.subheader("Reading Statistics")

    st.metric(
        "Reading Questions",
        stats["reading_total"]
    )

    st.metric(
        "Reading Correct",
        stats["reading_correct"]
    )

    if stats["reading_total"] > 0:

        reading_accuracy = (
            stats["reading_correct"]
            / stats["reading_total"]
        ) * 100

        st.metric(
            "Reading Accuracy",
            f"{reading_accuracy:.1f}%"
        )

    st.markdown("---")

    st.subheader("Grammar Statistics")

    st.metric(
        "Grammar Questions",
        stats["grammar_total"]
    )

    st.metric(
        "Grammar Correct",
        stats["grammar_correct"]
    )

    if stats["grammar_total"] > 0:

        grammar_accuracy = (
            stats["grammar_correct"]
            / stats["grammar_total"]
        ) * 100

        st.metric(
            "Grammar Accuracy",
            f"{grammar_accuracy:.1f}%"
        )

    st.markdown("---")

    vocab_count = len(
        load_vocabulary_topics()
    )

    st.metric(
        "Vocabulary Words Available",
        vocab_count
    )

    st.markdown("---")

    if st.button("Reset Progress"):

        st.session_state.stats = {
            "quiz_correct": 0,
            "quiz_total": 0,
            "reading_correct": 0,
            "reading_total": 0,
            "grammar_correct": 0,
            "grammar_total": 0
        }

        save_progress(
            st.session_state.stats
        )

        st.success(
            "Progress Reset Successfully"
        )

        st.rerun()

elif page == "Grammar Quiz":

    from app.grammar.grammar_quiz import get_grammar_question

    st.title("📝 Grammar Quiz")

    if "grammar_q" not in st.session_state:
        st.session_state.grammar_q = get_grammar_question()

    q = st.session_state.grammar_q

    st.subheader(
        q["question"]
    )

    answer = st.radio(
        "Choose",
        q["options"]
    )

    if st.button("Check"):

        st.session_state.stats["grammar_total"] += 1

        save_progress(
            st.session_state.stats
        )

        if answer == q["answer"]:

            st.session_state.stats["grammar_correct"] += 1

            save_progress(
                st.session_state.stats
            )

            st.success("✅ Correct")

        else:

            st.error(
                f"❌ Correct: {q['answer']}"
            )

    if st.button("Next"):

        st.session_state.grammar_q = (
            get_grammar_question()
        )

        st.rerun()


