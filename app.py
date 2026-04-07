# import streamlit as st
# import notepad
# import chat_assistant
# import rumination
# import song_suggester

# # ---------------- CONFIG ----------------
# st.set_page_config(
#     page_title="MindMate AI",
#     page_icon="🧠",
#     layout="wide"
# )

# # ---------------- HEADER ----------------
# st.markdown("""
# <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#             padding: 2rem;
#             border-radius: 20px;
#             text-align: center;
#             color: white;
#             margin-bottom: 2rem;">
#     <h1>🧠 MindMate AI</h1>
#     <p>A platform to express thoughts and analyze emotions</p>
# </div>
# """, unsafe_allow_html=True)

# # ---------------- SIDEBAR ----------------
# with st.sidebar:
#     st.title("Navigation")

#     choice = st.radio(
#         "Go to:",
#         [
#             "🏠 Dashboard",
#             "📝 Notepad",
#             "💬 Chat Assistant",
#             "🧠 Analysis",
#             "🎵 Music Mood"
#         ]
#     )

# # ---------------- DASHBOARD ----------------
# if choice == "🏠 Dashboard":

#     st.subheader("Welcome to MindMate AI")

#     col1, col2, col3 = st.columns(3)

#     col1.metric("💬 Chats", "Active")
#     col2.metric("📝 Notes", "Tracked")
#     col3.metric("🧠 Analysis", "Enabled")

#     st.markdown("---")

#     st.write("### Features")

#     st.write("""
# - 📝 Write your thoughts  
# - 💬 Chat with AI  
# - 🧠 Analyze emotions  
# - 🎵 Get music suggestions  
# """)

# # ---------------- NOTEPAD ----------------
# elif choice == "📝 Notepad":
#     notepad.show_notepad()

# # ---------------- CHAT ----------------
# elif choice == "💬 Chat Assistant":
#     chat_assistant.show_chat()

# # ---------------- ANALYSIS ----------------
# elif choice == "🧠 Analysis":
#     rumination.show_rumination()

# # ---------------- MUSIC ----------------
# elif choice == "🎵 Music Mood":
#     song_suggester.show_song_suggester()

# # ---------------- FOOTER ----------------
# st.markdown("---")
# st.markdown(
#     "<div style='text-align:center;'>MindMate AI – Emotional Intelligence System</div>",
#     unsafe_allow_html=True
# )

import streamlit as st
import requests
import json
import time
from datetime import datetime

import notepad
import chat_assistant
import health
import song_suggester
import rumination
from theme import (
    inject_css, page_hero, section_label, soft_divider,
    info_banner, metric_card, feature_card, mood_emoji
)

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MindMate AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "history" not in st.session_state:
    st.session_state.history = []

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
PAGES = {
    "Dashboard":      "🏠",
    "Notepad":        "📝",
    "Chat Assistant": "💬",
    "Analysis":       "🧠",
    "Health":         "❤️",
    "Music Mood":     "🎵",
}

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="logo-text">🧠 Mind<span>Mate</span></div>
        <div class="tagline">Your private wellness companion</div>
    </div>""", unsafe_allow_html=True)

    for pg, icon in PAGES.items():
        if st.button(f"{icon}  {pg}", key=f"nav_{pg}", use_container_width=True):
            st.session_state.page = pg
            st.rerun()

    soft_divider()
    info_banner("🔒", "100% Private · Powered by Ollama")

# ─────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────
page = st.session_state.page

# ════════════════════════════════════════════
# 🏠  DASHBOARD
# ════════════════════════════════════════════
if page == "Dashboard":
    page_hero(
        "🌿 Welcome to MindMate AI",
        "A calm, private space to express, explore, and understand your mind."
    )

    # Live stats from session history
    total   = len(st.session_state.history)
    avg_rum = (round(sum(e["rumination"] for e in st.session_state.history) / total, 1)
               if total else "—")
    avg_cla = (round(sum(e["clarity"] for e in st.session_state.history) / total, 1)
               if total else "—")

    c1, c2, c3, c4 = st.columns(4)
    with c1: metric_card("💬 CONVERSATIONS",  "Active",      "Chat module ready")
    with c2: metric_card("📝 JOURNAL ENTRIES", "Tracked",    "Notepad + DB")
    with c3: metric_card("🧠 ANALYSES",        str(total),   "This session")
    with c4: metric_card("🔒 PRIVACY",         "100%",       "Runs fully local")

    soft_divider()
    section_label("✨ EXPLORE FEATURES")

    r1c1, r1c2, r1c3 = st.columns(3)
    with r1c1:
        feature_card("📝", "Notepad Journal",
                     "Write personal thoughts and reflections in your private journal. Entries are saved locally.",
                     ["Private", "Thought tracking", "Auto-analysis"])
    with r1c2:
        feature_card("💬", "Chat Assistant",
                     "Have a warm, supportive conversation with the AI about anything on your mind.",
                     ["Empathetic AI", "Mood detection", "Pattern insight"])
    with r1c3:
        feature_card("🧠", "Mind & Emotion Analysis",
                     "Detect rumination patterns, emotional clarity, and cognitive load from your entries.",
                     ["phi3 / llama3", "Pattern detection", "Visualisation"])

    r2c1, r2c2, r2c3 = st.columns(3)
    with r2c1:
        feature_card("❤️", "Health & Wellbeing",
                     "Simple, practical tips and routines to support your mental and physical health every day.",
                     ["Daily tips", "Breathing", "Wellness"])
    with r2c2:
        feature_card("🎵", "Music Mood",
                     "Get song suggestions in Hindi & English curated to match or gently lift your mood.",
                     ["Hindi + English", "Mood-aware", "Uplifting"])
    with r2c3:
        feature_card("📊", "Insights & Trends",
                     "View your emotional patterns over time through clear charts and summaries.",
                     ["Charts", "Mood trends", "Progress"])

    soft_divider()

    # Recent analyses from this session
    if st.session_state.history:
        section_label("🕐 RECENT ANALYSES THIS SESSION")
        BADGE = {
            "Positive":    ("#edf7f0", "#2d7a4f", "#b8ddc5"),
            "Anxious":     ("#fdf2f2", "#a0444a", "#f0c0c2"),
            "Melancholic": ("#f0f0fc", "#4a4a9a", "#c0c0f0"),
            "Reflective":  ("#f7f4fc", "#6a4a9a", "#d0c0f0"),
            "Neutral":     ("#f4f5f0", "#5a6a4a", "#c4ceb4"),
        }
        for entry in reversed(st.session_state.history[-4:]):
            bg, fg, br = BADGE.get(entry.get("sentiment", "Neutral"),
                                   ("#f4f5f0", "#5a6a4a", "#c4ceb4"))
            st.markdown(f"""
            <div class="entry-card">
                <div class="ec-meta">
                    <span style="font-size:.8rem;color:#8fa48f;font-weight:600;">
                        🕐 {entry.get("timestamp","—")}
                    </span>
                    <span class="ec-mood" style="background:{bg};color:{fg};border:1px solid {br};">
                        {entry.get("sentiment","Neutral")}
                    </span>
                </div>
                <div class="ec-text">{entry.get("text_preview","—")}</div>
                <div class="ec-label">Key Theme</div>
                <div class="ec-analysis">{entry.get("key_theme","—")}</div>
            </div>""", unsafe_allow_html=True)
    else:
        info_banner("💡",
            "No analyses yet — head to Analysis, Notepad, or Chat to get started.")

    soft_divider()
    st.markdown(
        "<div style='text-align:center;color:#8fa48f;font-size:.8rem;font-weight:600;'>"
        "🧠 MindMate AI · Powered by Ollama (phi3 / llama3:8b) · "
        "Your thoughts never leave your device"
        "</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════
# 📝  NOTEPAD
# ════════════════════════════════════════════
elif page == "Notepad":
    page_hero("📝 Notepad Journal",
              "Your private space to write, reflect, and process your thoughts.")
    notepad.show_notepad()


# ════════════════════════════════════════════
# 💬  CHAT ASSISTANT
# ════════════════════════════════════════════
elif page == "Chat Assistant":
    page_hero("💬 Chat Assistant",
              "Talk through whatever's on your mind — no judgement, just support.")
    chat_assistant.show_chat()


# ════════════════════════════════════════════
# 🧠  ANALYSIS
# ════════════════════════════════════════════
elif page == "Analysis":
    page_hero("🧠 Mind & Emotion Analysis",
              "Understand your rumination patterns and emotional clarity over time.")
    rumination.show_rumination()


# ════════════════════════════════════════════
# ❤️  HEALTH
# ════════════════════════════════════════════
elif page == "Health":
    page_hero("❤️ Health & Wellbeing",
              "Simple daily habits for a healthier, calmer mind and body.")
    health.show_health_tips()


# ════════════════════════════════════════════
# 🎵  MUSIC MOOD
# ════════════════════════════════════════════
elif page == "Music Mood":
    page_hero("🎵 Music Mood",
              "Songs in Hindi & English selected to match or gently lift your mood.")
    song_suggester.show_song_suggester()


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
soft_divider()
st.markdown(
    "<div style='text-align:center;color:#8fa48f;font-size:.8rem;"
    "font-weight:600;padding-bottom:1rem;'>"
    "🧠 MindMate AI · Emotional Intelligence System · "
    "Private AI powered by Ollama · Your thoughts stay on your device"
    "</div>", unsafe_allow_html=True)
