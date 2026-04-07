import streamlit as st
from gtts import gTTS
import tempfile

# Function to convert text to speech
def speak_text(text, lang="en"):
    try:
        tts = gTTS(text=text, lang=lang)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        st.audio(temp_file.name, format="audio/mp3")
    except Exception as e:
        st.error(f"Speech generation error: {e}")

# Main function for the Song Suggester
def show_song_suggester():
    st.subheader("🎵 Music Mood Suggester")
    st.write("Tell me how you're feeling (English or Hindi), and I'll suggest a song 🎶")

    # User mood input
    mood = st.text_input("How are you feeling today?")

    if st.button("Suggest Song"):
        if mood:
            mood = mood.lower()

            # Mood to Song mapping with Hindi + English
            if "happy" in mood or "khush" in mood or "masti" in mood:
                song = "🙂 Happy Mood:\n- English: 'Happy - Pharrell Williams'\n- Hindi: 'Gallan Goodiyan - Dil Dhadakne Do'"
            elif "sad" in mood or "dukhi" in mood or "rona" in mood:
                song = "😢 Sad Mood:\n- English: 'Someone Like You - Adele'\n- Hindi: 'Channa Mereya - Ae Dil Hai Mushkil'"
            elif "love" in mood or "pyaar" in mood or "romantic" in mood:
                song = "❤️ Love Mood:\n- English: 'Perfect - Ed Sheeran'\n- Hindi: 'Tum Hi Ho - Aashiqui 2'"
            elif "angry" in mood or "gussa" in mood:
                song = "😡 Angry Mood:\n- English: 'Numb - Linkin Park'\n- Hindi: 'Bhaag DK Bose - Delhi Belly'"
            elif "relaxed" in mood or "calm" in mood or "shaant" in mood:
                song = "🌙 Relaxed Mood:\n- English: 'Fix You - Coldplay'\n- Hindi: 'Ilahi - Yeh Jawaani Hai Deewani'"
            elif "party" in mood or "dance" in mood:
                song = "🎉 Party Mood:\n- English: 'Uptown Funk - Bruno Mars'\n- Hindi: 'London Thumakda - Queen'"
            elif "motivated" in mood or "energy" in mood or "josh" in mood:
                song = "💪 Motivated Mood:\n- English: 'Eye of the Tiger - Survivor'\n- Hindi: 'Lakshya Title Song'"
            elif "nostalgic" in mood or "yaad" in mood:
                song = "✨ Nostalgic Mood:\n- English: 'See You Again - Wiz Khalifa'\n- Hindi: 'Tera Yaar Hoon Main - Sonu Ke Titu Ki Sweety'"
            else:
                song = "🌍 Default Mood:\n- English: 'On Top of the World - Imagine Dragons'\n- Hindi: 'Aaj Kal Zindagi - Wake Up Sid'"

            # Show suggestion
            st.success(f"🎶 Based on your mood, here are songs:\n\n{song}")

            # Speak suggestion (only English part spoken for clarity)
            speak_text("Here are some songs for you. " + song, "en")
        else:
            st.warning("⚠️ Please type how you're feeling first.")
