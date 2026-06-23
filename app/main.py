import streamlit as st

from app.data.content_loader import load_vocabulary_topics
from app.quizzes.quiz_engine import generate_question
from app.data.stats import initialize_stats
from gtts import gTTS
import os
from app.chatbot.german_tutor import ask_tutor
import pandas as pd
import matplotlib.pyplot as plt
from app.flashcards.flashcard_engine import get_flashcard
from app.reading.reading_engine import get_random_reading
from app.data.progress_manager import (
    load_progress,
    save_progress
)
from app.listening.listening_engine import (
    get_random_listening
)


st.set_page_config(
    page_title="GermanPath AI",
    page_icon="🇩🇪",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>

.main {
    background-color: #f8fafc;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    font-weight: bold;
}

.stMetric {
    border-radius: 12px;
    padding: 10px;
}

h1, h2, h3 {
    color: #0f172a;
}

</style>
""", unsafe_allow_html=True)

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
        "Listening",
        "Reading",
        "Goethe Exam",
        "AI Tutor",
        "Progress"
    ]
)
st.image(
    "https://images.unsplash.com/photo-1527866512907-a35a62a0f6c2",
    use_container_width=True
)
if page == "Home":

    st.title("🇩🇪 GermanPath AI")

    st.markdown("""
    ## Learn German Smarter

    Interactive German learning platform for
    Vocabulary, Grammar, Reading, Listening,
    and Goethe Exam Preparation.
    """)

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📚 Words", len(load_vocabulary_topics()))

    with col2:
        st.metric("📝 Quizzes", "100+")

    with col3:
        st.metric("📖 Readings", "10+")

    with col4:
        st.metric("🎧 Listening", "10+")

    st.markdown("---")

    st.subheader("Available Modules")

    st.write("• Vocabulary")
    st.write("• Flashcards")
    st.write("• Grammar")
    st.write("• Quick Quiz")
    st.write("• Practice Test")
    st.write("• Mock Exam")
    st.write("• Reading Practice")
    st.write("• Listening Practice")
    st.write("• Progress Tracking")

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

            st.markdown(
            f"""
            <div style="
                padding:15px;
                border-radius:15px;
                background-color:#ffffff;
                margin-bottom:10px;
                border:1px solid #d1d5db;
                box-shadow:0 2px 5px rgba(0,0,0,0.05);
            ">
                <h4>🇩🇪 {word['german']}</h4>
                <p>🇬🇧 {word['english']}</p>
            </div>
            """,
            unsafe_allow_html=True
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

elif page == "Listening":

    from app.listening.listening_engine import (
        get_random_listening
    )

    from gtts import gTTS
    import os

    st.title("🎧 Listening Practice")

    if "listening" not in st.session_state:

        st.session_state.listening = (
            get_random_listening()
        )

    item = st.session_state.listening

    audio_file = "temp_listening.mp3"

    tts = gTTS(
        text=item["transcript"],
        lang="de"
    )

    tts.save(audio_file)

    st.audio(audio_file)

    st.markdown("---")

    st.subheader(
        item["question"]
    )

    answer = st.radio(
        "Choose an answer",
        item["options"]
    )

    if st.button(
        "Check Listening Answer"
    ):

        st.session_state.stats[
            "listening_total"
        ] += 1

        if answer == item["answer"]:

            st.session_state.stats[
                "listening_correct"
            ] += 1

            st.success(
                "✅ Correct!"
            )

        else:

            st.error(
                f"❌ Correct Answer: {item['answer']}"
            )

    if st.button(
        "Show Transcript"
    ):

        st.info(
            item["transcript"]
        )

    if st.button(
        "Next Listening"
    ):

        if os.path.exists(
            audio_file
        ):

            os.remove(
                audio_file
            )

        st.session_state.listening = (
            get_random_listening()
        )

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
elif page == "Goethe Exam":

    st.title("🎓 Goethe A1 Mock Exam")

    st.info(
        """
        Exam Structure

        📖 Reading : 5 Questions
        🎧 Listening : 5 Questions
        📝 Grammar : 5 Questions

        Total: 15 Questions
        """
    )

    st.metric(
        "Passing Score",
        "60%"
    )

    if st.button(
        "Start Exam"
    ):
        st.success(
            "🚀 Goethe Exam Mode Started"
        )
elif page == "Progress":

    st.title("📊 Progress Dashboard")

stats = st.session_state.stats

col1, col2 = st.columns(2)

with col1:

    st.subheader("📝 Quiz")

    st.metric(
        "Questions Attempted",
        stats.get("quiz_total", 0)
    )

    st.metric(
        "Correct Answers",
        stats.get("quiz_correct", 0)
    )

    if stats.get("quiz_total", 0) > 0:

        st.metric(
            "Accuracy",
            f"{(stats['quiz_correct']/stats['quiz_total'])*100:.1f}%"
        )

with col2:

    st.subheader("📖 Reading")

    st.metric(
        "Questions",
        stats.get("reading_total", 0)
    )

    st.metric(
        "Correct",
        stats.get("reading_correct", 0)
    )

    if stats.get("reading_total", 0) > 0:

        st.metric(
            "Accuracy",
            f"{(stats['reading_correct']/stats['reading_total'])*100:.1f}%"
        )

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    st.subheader("🎧 Listening")

    st.metric(
        "Questions",
        stats.get("listening_total", 0)
    )

    st.metric(
        "Correct",
        stats.get("listening_correct", 0)
    )

    if stats.get("listening_total", 0) > 0:

        st.metric(
            "Accuracy",
            f"{(stats['listening_correct']/stats['listening_total'])*100:.1f}%"
        )

with col2:

    st.subheader("🇩🇪 Grammar")

    st.metric(
        "Questions",
        stats.get("grammar_total", 0)
    )

    st.metric(
        "Correct",
        stats.get("grammar_correct", 0)
    )

    if stats.get("grammar_total", 0) > 0:

        st.metric(
            "Accuracy",
            f"{(stats['grammar_correct']/stats['grammar_total'])*100:.1f}%"
        )

st.markdown("---")

vocab_count = len(
    load_vocabulary_topics()
)

st.metric(
    "📚 Vocabulary Words Available",
    vocab_count
)

st.markdown("---")

if st.button("🔄 Reset Progress"):

    st.session_state.stats = {
        "quiz_correct": 0,
        "quiz_total": 0,
        "reading_correct": 0,
        "reading_total": 0,
        "grammar_correct": 0,
        "grammar_total": 0,
        "listening_correct": 0,
        "listening_total": 0
    }

    save_progress(
        st.session_state.stats
    )

    st.success(
        "Progress Reset Successfully"
    )

    st.rerun()

elif page == "AI Tutor":

    from app.chatbot.german_tutor import ask_tutor

    st.title("🤖 German AI Tutor")

    question = st.text_input(
        "Ask anything about German"
    )

    if st.button("Ask"):

        with st.spinner(
            "Thinking..."
        ):

            answer = ask_tutor(
                question
            )

        st.markdown(answer)

