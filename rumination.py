import streamlit as st
import matplotlib.pyplot as plt
from database import get_all_data
from analysis_utils import analyze_text


def show_rumination():

    st.header("🧠 Mind & Emotion Analysis")

    # 🔹 Fetch data
    history = get_all_data()

    if not history:
        st.warning("No data available yet. Please use Chat or Notepad first.")
        return

    # 🔹 Combine all text
    combined_text = " ".join([row[1] for row in history])

    if not combined_text.strip():
        st.warning("⚠️ No text available for analysis.")
        return

    # 🔥 AI Analysis
    rumination_analysis, emotional_analysis = analyze_text(combined_text)

    rumination_analysis = rumination_analysis or "No rumination data"
    emotional_analysis = emotional_analysis or "No emotional data"

    # 🔥 IMPROVED SCORE LOGIC
    total_entries = len(history)

    # Score based on repeated entries (pattern)
    score = min(total_entries * 2, 10)

    if score < 4:
        level = "Low"
    elif score < 7:
        level = "Moderate"
    else:
        level = "High"

    # 🔥 SELECTOR
    option = st.radio(
        "Choose Analysis Type:",
        ["🧠 Rumination", "💬 Emotional", "📊 Visualization"],
        horizontal=True
    )

    # -------------------------------
    # 🧠 RUMINATION SECTION
    # -------------------------------
    if option == "🧠 Rumination":
        st.subheader("🧠 Rumination Analysis")

        st.info(rumination_analysis)

        st.success(f"Level: {level} | Score: {score}/10")

        st.caption(f"Based on {total_entries} entries")

    # -------------------------------
    # 💬 EMOTIONAL SECTION
    # -------------------------------
    elif option == "💬 Emotional":
        st.subheader("💬 Emotional Clarity")

        st.info(emotional_analysis)

    # -------------------------------
    # 📊 VISUALIZATION SECTION
    # -------------------------------
    elif option == "📊 Visualization":
        st.subheader("📊 Mental State Visualization")

        fig, ax = plt.subplots()

        values = [score, 10 - score]
        labels = ["Mental Load", "Stable"]

        ax.pie(
            values,
            labels=labels,
            autopct='%1.0f%%'
        )

        ax.set_title(f"Mental State: {level}")

        st.pyplot(fig)

        # 🔥 Extra insight
        st.markdown("### 🧠 Insight")
        st.write(f"You have made **{total_entries} entries**, indicating your mental tracking consistency.")
