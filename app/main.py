import streamlit as st

from app.data.vocabulary_engine import get_a1_words
from app.data.a1_dictionary import A1_DICTIONARY

st.set_page_config(
    page_title="GermanPath AI",
    page_icon="🇩🇪",
    layout="wide"
)

st.sidebar.title("🇩🇪 GermanPath AI")

page = st.sidebar.radio(
    "Navigation",
    ["Home", "Vocabulary", "Progress"]
)

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

elif page == "Vocabulary":

    st.title("📚 A1 Vocabulary")

    words = get_a1_words(20)

    for word in words:
        meaning = A1_DICTIONARY.get(
            word,
            "Meaning not found"
        )

        st.success(
            f"{word} → {meaning}"
        )

elif page == "Progress":

    st.title("🎯 Progress Tracker")

    st.progress(25)

    st.metric(
        "Vocabulary Learned",
        "20 Words"
    )

    st.metric(
        "Current Level",
        "A1"
    )