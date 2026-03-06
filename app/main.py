from speech.speech_text_transform import speech_to_text, text_to_speech
import datetime
import webbrowser
import os
import sys
import joblib
import warnings
import numpy as np
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from sklearn.exceptions import InconsistentVersionWarning
from core.llm_intent_mapper import llm_predict_intent

# =========================
# CONFIG
# =========================
CONFIDENCE_THRESHOLD = 0.75
warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

# =========================
# SHORT-TERM MEMORY
# =========================
memory = {
    "last_intent": None,
    "last_platform": None
}

# =========================
# LOAD MODEL & SCALER
# =========================
try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    stack_clf = joblib.load(os.path.join(base_dir, "jarvis_intent_model_stack.pkl"))
    scaler = joblib.load(os.path.join(base_dir, "jarvis_scaler_stack.pkl"))
except Exception as e:
    print(f"❌ Model load failed: {e}")
    sys.exit(1)

# =========================
# LOAD SPACY
# =========================
try:
    nlp = spacy.load("en_core_web_md")
except OSError:
    print("❌ Run: python -m spacy download en_core_web_md")
    sys.exit(1)

stopwords = set(STOP_WORDS)

# =========================
# INTENT IDS
# =========================
GET_TIME = 0
SEARCH_GOOGLE = 1
SEARCH_YOUTUBE = 2
OPEN_NOTEPAD = 3
OPEN_CALCULATOR = 4
OPEN_WHATSAPP = 5
OPEN_LINKEDIN = 6
OPEN_GITHUB = 7
OPEN_SPOTIFY = 8
EXIT_INTENT = 9

INTENT_NAME_TO_ID = {
    "get_time": GET_TIME,
    "search_google": SEARCH_GOOGLE,
    "search_youtube": SEARCH_YOUTUBE,
    "open_notepad": OPEN_NOTEPAD,
    "open_calculator": OPEN_CALCULATOR,
    "open_whatsapp": OPEN_WHATSAPP,
    "open_linkedin": OPEN_LINKEDIN,
    "open_github": OPEN_GITHUB,
    "open_spotify": OPEN_SPOTIFY,
    "exit": EXIT_INTENT
}

INTENT_PLATFORM_MAP = {
    SEARCH_GOOGLE: "google",
    SEARCH_YOUTUBE: "youtube",
    OPEN_SPOTIFY: "spotify"
}

# =========================
# ML INTENT PREDICTION
# =========================
def find_intent(command: str):
    if not command.strip():
        return -1, 0.0

    command_clean = " ".join(
        word for word in command.lower().split() if word not in stopwords
    )
    doc = nlp(command_clean)

    if not np.any(doc.vector):
        return -1, 0.0

    try:
        vector = scaler.transform(doc.vector.reshape(1, -1))
        probs = stack_clf.predict_proba(vector)[0]
        return int(np.argmax(probs)), float(np.max(probs))
    except Exception:
        return -1, 0.0

# =========================
# CONTEXT HELPERS
# =========================
def is_vague_command(command: str):
    return any(
        word in command.lower()
        for word in ["play", "watch", "listen", "search", "show"]
    )

def infer_from_context():
    platform = memory.get("last_platform")

    if platform == "youtube":
        return SEARCH_YOUTUBE
    if platform == "google":
        return SEARCH_GOOGLE
    if platform == "spotify":
        return OPEN_SPOTIFY

    return None

# =========================
# EXECUTION
# =========================
def execute_intent(intent: int):
    global memory

    try:
        if intent == GET_TIME:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            text_to_speech(f"The current time is {now}")
            return f"The current time is {now}"

        elif intent == SEARCH_GOOGLE:
            webbrowser.open("https://www.google.com/")
            text_to_speech("Opening Google")

        elif intent == SEARCH_YOUTUBE:
            webbrowser.open("https://www.youtube.com/")
            text_to_speech("Opening YouTube")

        elif intent == OPEN_NOTEPAD:
            webbrowser.open("https://editpad.org/")
            text_to_speech("Opening Notepad")

        elif intent == OPEN_CALCULATOR:
            webbrowser.open("https://www.google.com/search?q=online+calculator")
            text_to_speech("Opening Calculator")

        elif intent == OPEN_WHATSAPP:
            webbrowser.open("https://web.whatsapp.com/")
            text_to_speech("Opening WhatsApp")

        elif intent == OPEN_LINKEDIN:
            webbrowser.open("https://www.linkedin.com/")
            text_to_speech("Opening LinkedIn")

        elif intent == OPEN_GITHUB:
            webbrowser.open("https://github.com/")
            text_to_speech("Opening GitHub")

        elif intent == OPEN_SPOTIFY:
            webbrowser.open("https://open.spotify.com/")
            text_to_speech("Opening Spotify")

        elif intent == EXIT_INTENT:
            text_to_speech("Goodbye.")
            sys.exit(0)

        # 🔹 Update context memory
        if intent in INTENT_PLATFORM_MAP:
            memory["last_intent"] = intent
            memory["last_platform"] = INTENT_PLATFORM_MAP[intent]

        return "Done"

    except Exception as e:
        print(f"⚠️ Execution error: {e}")
        return "Something went wrong."

# =========================
# CENTRAL BRAIN
# =========================
def process_command(command: str):
    intent, confidence = find_intent(command)
    print(f"🔍 ML Intent: {intent}, Confidence: {confidence:.2f}")

    # 1️⃣ ML confident
    if confidence >= CONFIDENCE_THRESHOLD and intent != -1:
        return execute_intent(intent)

    # 2️⃣ Context-based inference
    if is_vague_command(command):
        inferred = infer_from_context()
        if inferred is not None:
            print("🧠 Using contextual memory")
            return execute_intent(inferred)

    # 3️⃣ LLM fallback
    print("🤖 Switching to LLM fallback...")
    llm_intent = llm_predict_intent(command)
    print(f"🧠 LLM Intent: {llm_intent}")

    if llm_intent in INTENT_NAME_TO_ID:
        return execute_intent(INTENT_NAME_TO_ID[llm_intent])

    return "Sorry, I couldn't understand that."

# =========================
# TERMINAL MODE
# =========================
if __name__ == "__main__":
    text_to_speech("Jarvis is online.")
    print("Listening...")

    while True:
        try:
            command = speech_to_text()
            if not command:
                continue

            print(f"🎤 You said: {command}")
            process_command(command)

        except KeyboardInterrupt:
            text_to_speech("Goodbye.")
            sys.exit(0)
