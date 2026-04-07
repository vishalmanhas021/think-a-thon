import streamlit as st
import google.generativeai as genai
from analysis_utils import detect_rumination, detect_emotion_clarity
from database import init_db, save_full_data, get_all_data

# Model configuration
model = genai.GenerativeModel("gemini-2.5-flash")


# 🔥 Mood detection
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


# 🔥 Pattern analysis
def analyze_pattern(history):
    moods = [row[2] for row in history]

    if not moods:
        return "No data available yet."

    if moods.count("sad") >= 3:
        return "You seem to be feeling low for quite some time."
    elif moods.count("anxiety") >= 2:
        return "You may be experiencing repeated anxiety."
    elif "happy" in moods and moods[-1] == "happy":
        return "Your mood seems to be improving."
    else:
        return "Your mood appears relatively stable."


# 🔥 AI Response
def get_ai_response(prompt):
    try:
        response = model.generate_content(prompt)

        if response and getattr(response, "text", None):
            return response.text.strip()

        return "💙 I’m here with you. Tell me what’s on your mind."

    except Exception as exc:
        st.error(f"AI service error: {exc}")
        return "💙 I’m here with you. Tell me what’s on your mind."


# 🔥 MAIN CHAT FUNCTION
def show_chat():

    st.header("💬 Chat Assistant")

    init_db()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Show chat
    for sender, message in st.session_state.chat_history:
        with st.chat_message("user" if sender == "You" else "assistant"):
            st.write(message)

    user_message = st.chat_input("Share your thoughts...")

    if user_message:

        # STEP 1: Mood detection
        mood = detect_mood(user_message)

        # STEP 2: Analyze current message
        rumination = detect_rumination(user_message)
        emotion = detect_emotion_clarity(user_message)

        # STEP 3: Save in DB
        save_full_data(user_message, mood, rumination, emotion)

        st.session_state.chat_history.append(("You", user_message))

        with st.chat_message("user"):
            st.write(user_message)

        # STEP 4: Get history
        history = get_all_data()

        # STEP 5: Combine all messages
        combined_text = " ".join([row[1] for row in history])

        # STEP 6: Final analysis (current + past)
        final_rumination = detect_rumination(combined_text)
        final_emotion = detect_emotion_clarity(combined_text)

        # ✅ SHOW ONLY FINAL RESULT
        st.markdown("### 🧠 Overall Analysis")
        st.info(final_rumination)
        st.info(final_emotion)

        # STEP 7: Pattern insight
        insight = analyze_pattern(history)

        # STEP 8: AI response context
        history_text = ""
        for row in history[-5:]:
            history_text += f"{row[1]} ({row[2]})\n"

        final_prompt = f"""
User previous messages:
{history_text}

Current message:
{user_message}

Detected mood: {mood}

Pattern insight: {insight}

Respond like a supportive mental health assistant.
"""

        reply = get_ai_response(final_prompt)

        st.session_state.chat_history.append(("MindMate AI", reply))

        with st.chat_message("assistant"):
            st.write(reply)

        # Show insight
        st.markdown("### 🧠 Pattern Insight")
        st.success(insight)

    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()