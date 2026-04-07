import streamlit as st
import random

def show_health_tips():
    st.header("🍀 Health & Wellness Tips")

    tips = [
        "Drink at least 8 glasses of water today 💧",
        "Take a 5-minute break and stretch 🧘",
        "Go for a short walk 🚶",
        "Eat fresh fruits and vegetables 🍎",
        "Take 3 deep breaths and relax 🌬"
    ]

    if st.button("Show Health Tip"):
        st.info(random.choice(tips))
