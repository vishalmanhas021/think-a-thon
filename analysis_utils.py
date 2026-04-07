import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3"


def analyze_text(text):

    prompt = f"""
You are an expert mental health assistant.

Analyze the text deeply.

STRICT RULES:
- Follow the format EXACTLY
- Do not add extra text
- Do not skip sections

FORMAT:

Rumination:
Level: Yes or No
Explanation: 1-2 lines

Emotional Clarity:
Level: Low, Medium, or High
Explanation: 1-2 lines

Text:
"{text}"
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,   # ✅ use variable
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "max_tokens": 150
                }
            },
            timeout=60
        )

        print("STATUS CODE:", response.status_code)

        if response.status_code == 200:
            data = response.json()
            full_response = data.get("response", "").strip()

            print("🔍 RAW RESPONSE:\n", full_response)

            if not full_response:
                return "⚠️ Empty rumination", "⚠️ Empty emotional clarity"

            # ✅ robust parsing
            if "Emotional Clarity" in full_response:
                parts = full_response.split("Emotional Clarity", 1)

                rumination_part = parts[0].strip()
                emotional_part = "Emotional Clarity" + parts[1].strip()
            else:
                rumination_part = full_response
                emotional_part = "⚠️ Emotional clarity not detected"

            return rumination_part, emotional_part

    except Exception as e:
        print("❌ ERROR:", e)

    return "⚠️ No rumination data", "⚠️ No emotional data"