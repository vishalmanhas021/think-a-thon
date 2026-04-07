import streamlit as st
import requests
from analysis_utils import analyze_text
from database import init_db, save_full_data, get_all_data

# 🔥 Ollama API
OLLAMA_URL = "http://localhost:11434/api/generate"


# 🔥 Improved Mood Detection
def detect_mood(text):
    text = text.lower()

    # handle negations (important fix)
    if "not sad" in text or "not depressed" in text:
        return "neutral"

    sad_words = ["sad", "depressed", "low", "tired", "hopeless"]
    happy_words = ["happy", "good", "better", "great", "fine"]
    anxiety_words = ["anxious", "worried", "stress", "panic", "overthinking"]

    if any(word in text for word in sad_words):
        return "sad"
    elif any(word in text for word in anxiety_words):
        return "anxiety"
    elif any(word in text for word in happy_words):
        return "happy"
    else:
        return "neutral"


# 🔥 Pattern Analysis
def analyze_pattern(history):
    moods = [row[2] for row in history]

    if not moods:
        return "No data available yet."

    if moods.count("sad") >= 3:
        return "You seem to be feeling low for quite some time."
    elif moods.count("anxiety") >= 2:
        return "You may be experiencing repeated anxiety."
    elif moods[-1] == "happy":
        return "Your mood seems to be improving."
    else:
        return "Your mood appears relatively stable."


# 🔥 Ollama Response Function
def get_ai_response(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3:8b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.5,
                    "top_p": 0.9,
                    "max_tokens": 200
                }
            },
            timeout=20
        )

        if response.status_code == 200:
            data = response.json()
            return data.get("response", "").strip()

    except Exception as e:
        print("Ollama error:", e)

    return "💙 I'm here with you. Tell me what's on your mind."


# 🔥 MAIN CHAT FUNCTION
def show_chat():

    st.header("💬 MindMate AI Chat Assistant")

    init_db()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # 🔹 Show previous messages
    for sender, message in st.session_state.chat_history:
        with st.chat_message("user" if sender == "You" else "assistant"):
            st.write(message)

    user_message = st.chat_input("Share your thoughts...")

    if user_message:

        # STEP 1: Mood Detection
        mood = detect_mood(user_message)

        st.session_state.chat_history.append(("You", user_message))

        with st.chat_message("user"):
            st.write(user_message)

        # STEP 2: Get past history
        history = get_all_data()
        past_text = " ".join([row[1] for row in history])

        # 🔥 Better context formatting
        combined_text = f"""
Past thoughts:
{past_text}

Current thought:
{user_message}
"""

        # STEP 3: Analysis
        rumination_analysis, emotional_analysis = analyze_text(combined_text)

        rumination_analysis = rumination_analysis or "No rumination data"
        emotional_analysis = emotional_analysis or "No emotional data"

        # STEP 4: Save
        save_full_data(user_message, mood, rumination_analysis, emotional_analysis)

        # 🔹 Show Analysis
        st.markdown("### 🧠 Rumination Analysis")
        st.info(rumination_analysis)

        st.markdown("### 💬 Emotional Clarity")
        st.info(emotional_analysis)

        st.caption(f"Detected Mood: {mood}")

        # STEP 5: Pattern Insight
        updated_history = get_all_data()
        insight = analyze_pattern(updated_history)

        # STEP 6: Prepare history context
        history_text = ""
        for row in updated_history[-5:]:
            history_text += f"{row[1]} ({row[2]})\n"

        # 🔥 Improved Prompt
        final_prompt = f"""
You are a compassionate and emotionally intelligent mental health assistant.

IMPORTANT RULES:
- Be supportive, not clinical
- Do NOT sound robotic
- Keep response short (3-5 lines max)
- Do NOT give medical advice

User past messages:
{history_text}

Current message:
{user_message}

Detected mood: {mood}
Pattern insight: {insight}

Your response should include:
1. Emotional validation
2. Understanding
3. One small helpful suggestion

Tone: warm, human, supportive
"""

        # STEP 7: AI Response
        reply = get_ai_response(final_prompt)

        st.session_state.chat_history.append(("MindMate AI", reply))

        with st.chat_message("assistant"):
            st.write(reply)

        # 🔹 Suggestion
        st.markdown("### 💡 Suggested Action")
        st.write("Try deep breathing, journaling, or a short walk.")

        # 🔹 Pattern Insight
        st.markdown("### 🧠 Pattern Insight")
        st.success(insight)

    # 🔹 Clear Chat
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()
