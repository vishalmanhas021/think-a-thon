import streamlit as st
import datetime
import requests
import re

from analysis_utils import analyze_text
from database import init_db, save_full_data

OLLAMA_URL = "http://localhost:11434/api/generate"


# 🔥 STRONG CLEAN FUNCTION (FINAL)
def clean_text(text):
    if not text:
        return ""

    # remove ALL html tags
    text = re.sub(r'<.*?>', '', text)

    # remove unwanted labels
    text = text.replace("🧠 Rumination:", "")
    text = text.replace("💬 Emotional Clarity:", "")
    text = text.replace("Rumination:", "")
    text = text.replace("Emotional Clarity:", "")

    # remove extra spaces/newlines
    text = re.sub(r'\n+', '\n', text)

    return text.strip()


# 🧠 Mood Detection (Ollama)
def detect_mood(text):
    prompt = f"""
Return ONLY one word: sad / happy / anxiety / neutral

Text: "{text}"
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3:8b",
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.2}
            },
            timeout=10
        )

        if response.status_code == 200:
            mood = response.json().get("response", "").strip().lower()
            if mood in ["sad", "happy", "anxiety", "neutral"]:
                return mood

    except:
        pass

    return "neutral"


# 😊 Sentiment words
def detect_sentiment_words(text):
    prompt = f"""
Positive: words
Negative: words

Text: "{text}"
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3:8b",
                "prompt": prompt,
                "stream": False
            },
            timeout=10
        )

        if response.status_code == 200:
            result = response.json().get("response", "")

            pos, neg = [], []

            for line in result.split("\n"):
                if "Positive:" in line:
                    pos = [w.strip() for w in line.replace("Positive:", "").split(",") if w.strip()]
                if "Negative:" in line:
                    neg = [w.strip() for w in line.replace("Negative:", "").split(",") if w.strip()]

            return pos, neg

    except:
        pass

    return [], []


# 📝 MAIN
def show_notepad():

    init_db()

    if 'saved_thoughts' not in st.session_state:
        st.session_state.saved_thoughts = []

    st.header("📝 Mindful Journal")

    thought_content = st.text_area("How are you feeling today?", height=200)

    if st.button("💾 Save Entry"):

        if thought_content.strip():

            mood = detect_mood(thought_content)

            # 🔥 ANALYSIS
            rumination, emotion = analyze_text(thought_content)

            # 🔥 CLEAN BEFORE SAVE
            rumination = clean_text(rumination)
            emotion = clean_text(emotion)

            pos_words, neg_words = detect_sentiment_words(thought_content)

            save_full_data(thought_content, mood, rumination, emotion)

            st.success("✅ Saved & analyzed successfully!")

            # 🔥 CLEAN DISPLAY
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🧠 Rumination")
                st.success(rumination)

            with col2:
                st.subheader("💬 Emotional Clarity")
                st.info(emotion)

            st.subheader("😊 Sentiment")
            st.write("Positive:", pos_words if pos_words else "None")
            st.write("Negative:", neg_words if neg_words else "None")

        else:
            st.warning("Write something first")

    # 📚 DISPLAY
    data = []

    try:
        from database import get_all_data
        data = get_all_data()
    except:
        pass

    if data:
        st.subheader("📚 Your Entries")

        for row in data:
            text = row[1]
            mood = row[2]
            rumination = clean_text(row[3])
            emotion = clean_text(row[4])

            st.markdown(f"""
            **🧠 Mood:** {mood}  
            **📝 Text:** {text}  

            **🧠 Rumination:**  
            {rumination}  

            **💬 Emotional Clarity:**  
            {emotion}  
            """)
            st.divider()

    else:
        st.info("No entries yet")