import streamlit as st
import datetime
import json

# 🔥 IMPORT ANALYSIS + DATABASE
from analysis_utils import detect_rumination, detect_emotion_clarity
from database import init_db, save_full_data


# 🔥 Mood detection (same as chat)
def detect_mood(text):
    text = text.lower()

    if any(word in text for word in ["sad", "depressed", "low"]):
        return "sad"
    elif any(word in text for word in ["happy", "good", "better"]):
        return "happy"
    elif any(word in text for word in ["anxious", "worried", "stress"]):
        return "anxiety"
    else:
        return "neutral"


def show_notepad():

    # 🔥 Initialize DB
    init_db()

    # CSS styling (same as yours)
    st.markdown("""
    <style>
    .notepad-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .thought-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
    }
    </style>
    """, unsafe_allow_html=True)

    # Session state
    if 'saved_thoughts' not in st.session_state:
        st.session_state.saved_thoughts = []

    # Header
    st.markdown("""
    <div class="notepad-header">
        <h1>📝 Mindful Journal</h1>
        <p>Write your thoughts freely</p>
    </div>
    """, unsafe_allow_html=True)

    # Input section
    thought_content = st.text_area(
        "How are you feeling today?",
        height=200
    )

    word_count = len(thought_content.split())

    # Save button
    if st.button("💾 Save Entry"):

        if thought_content.strip():

            # 🔥 STEP 1: Detect mood
            mood = detect_mood(thought_content)

            # 🔥 STEP 2: Rumination
            rumination = detect_rumination(thought_content)

            # 🔥 STEP 3: Emotional clarity
            emotion = detect_emotion_clarity(thought_content)

            # 🔥 STEP 4: Save to DB (IMPORTANT)
            save_full_data(thought_content, mood, rumination, emotion)

            # Save locally for display
            entry = {
                "content": thought_content,
                "mood": mood,
                "rumination": rumination,
                "emotion": emotion,
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "words": word_count
            }

            st.session_state.saved_thoughts.insert(0, entry)

            st.success("✅ Saved & analyzed successfully!")

            # 🔥 SHOW RESULTS INSTANTLY
            st.markdown("### 🧠 Analysis Result")
            st.info(f"Rumination: {rumination}")
            st.info(f"Emotional Clarity: {emotion}")

        else:
            st.warning("⚠️ Please write something first")

    # Display saved thoughts
    if st.session_state.saved_thoughts:

        st.markdown("### 📚 Your Entries")

        for i, thought in enumerate(st.session_state.saved_thoughts):

            st.markdown(f"""
            <div class="thought-card">
                <b>📅 {thought['date']}</b><br>
                🧠 Mood: {thought['mood']}<br><br>
                {thought['content']}<br><br>
                <b>Rumination:</b> {thought['rumination']}<br>
                <b>Emotion:</b> {thought['emotion']}
            </div>
            """, unsafe_allow_html=True)

            if st.button("🗑️ Delete", key=i):
                st.session_state.saved_thoughts.pop(i)
                st.rerun()

    else:
        st.info("No entries yet. Start writing ✍️")