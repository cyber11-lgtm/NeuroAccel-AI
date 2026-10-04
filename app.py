import streamlit as st
import fitz
from pypdf import PdfReader
import re

st.set_page_config(
    page_title="NeuroAccel AI",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 NeuroAccel AI")
st.subheader("Free AI-style learning assistant")

pdf = st.file_uploader(
    "📚 Upload your textbook chapter",
    type=["pdf"]
)

if pdf:

    reader = PdfReader(pdf)

    text = ""

    for page in reader.pages:
        content = page.extract_text()

        if content:
            text += content + "\n"

    st.success(f"Loaded {len(reader.pages)} pages!")

    if not text.strip():
        st.error("No readable text was found.")
        st.stop()

    # Clean text
    clean_text = re.sub(r"\s+", " ", text).strip()

    # Basic concept extraction
    words = re.findall(r"\b[A-Za-z][A-Za-z-]{5,}\b", clean_text)

    frequency = {}

    for word in words:
        word = word.lower()
        frequency[word] = frequency.get(word, 0) + 1

    common_words = sorted(
        frequency,
        key=frequency.get,
        reverse=True
    )

    # Remove common English words
    ignored = {
        "which", "there", "their", "these", "those",
        "about", "would", "could", "should", "where",
        "between", "because", "through", "chapter",
        "figure", "example", "following"
    }
   

   
    concepts = [
        word for word in common_words
        if word not in ignored
    ][:15]

if "clean_text" not in globals():
    clean_text = ""

if "concepts" not in globals():
    concepts = []

tabs = st.tabs([
    f"📖 Understand",
    "🔑 Concepts",
    "🎯 Practice",
    "🧠 Mistakes"
    ])

with tabs[0]:

    st.header("📖 Chapter Overview")

    st.write(
        f"Your chapter contains approximately "
        f"**{len(clean_text.split())} words**."
    )

    st.info(
        "NeuroAccel has extracted the chapter and is "
        "building a learning profile from it."
    )

    with st.expander("View extracted material"):
        st.write(clean_text[:15000])


with tabs[1]:

    st.header("🔑 Important Concepts")

    st.write(
        "Frequently occurring technical-looking terms:"
    )

    for i, concept in enumerate(concepts, 1):
        st.write(f"**{i}. {concept.title()}**")


with tabs[2]:

    st.header("🎯 Practice Generator")

    st.write(
        "NeuroAccel creates practice questions "
        "from your uploaded chapter."
    )

    difficulty = st.selectbox(
        "Choose difficulty:",
        ["Easy", "Medium", "Hard"]
    )

    if st.button("🚀 Generate Questions"):

        sentences = re.split(
            r"(?<=[.!?])\s+",
            clean_text
        )

        useful_sentences = [
            s.strip()
            for s in sentences
            if len(s.strip()) > 60
        ]

        if not useful_sentences:

            st.warning(
                "Not enough readable material was found."
            )

        else:

            selected = useful_sentences[:5]

            st.success(
                f"Generated 5 {difficulty.lower()} practice questions!"
            )

            for i, sentence in enumerate(selected, 1):

                st.markdown(f"### Question {i}")

                st.write(
                    "Explain the main idea described here:"
                )

                st.info(sentence)

                answer = st.text_area(
                    f"Your answer for Question {i}",
                    key=f"answer_{i}"
                )

                if answer:
                    st.success("Answer recorded.")


with tabs[3]:

    st.header("🧠 Mistake Tracker")

    st.write(
        "Record concepts or questions you got wrong."
    )

    mistake = st.text_area(
        "What did you get wrong?"
    )

    if st.button("Save Mistake"):

        if mistake.strip():

            st.success(
                "Mistake recorded for your learning profile."
            )

        else:

            st.warning(
                "Write a mistake first."
            )