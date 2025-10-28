from speech_text_transform import speech_to_text, text_to_speech
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

# 🧠 Ignore sklearn warnings
warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

# 1️⃣ Load trained stacking model and scaler
try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "jarvis_intent_model_stack.pkl")
    scaler_path = os.path.join(base_dir, "jarvis_scaler_stack.pkl")

    stack_clf = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
except Exception as e:
    print(f"⚠️ Error loading model or scaler: {e}")
    sys.exit("❌ Exiting due to model load failure")

# 2️⃣ Load spaCy model and stopwords
try:
    nlp = spacy.load("en_core_web_md")
except OSError:
    print("⚠️ SpaCy model not found! Run: python -m spacy download en_core_web_md")
    sys.exit()

stopwords = set(STOP_WORDS)

# 3️⃣ Define intent constants
GET_TIME = 0
SEARCH_GOOGLE = 1
SEARCH_YOUTUBE = 2
OPEN_NOTEPAD = 3
OPEN_CALCULATOR = 4
OPEN_WHATSAPP = 5
OPEN_LINKEDIN = 6
OPEN_GITHUB = 7
OPEN_SPOTIFY = 8
EXIT_INTENT = 9  # avoid using Python keyword 'exit'


# 4️⃣ Function to predict intent
def find_intent(command: str) -> int:
    """Predicts the intent from a voice/text command."""
    if not command.strip():
        return -1

    # Remove stopwords
    command_clean = " ".join(
        [word for word in command.lower().split() if word not in stopwords]
    )

    # Convert to vector using spaCy
    doc = nlp(command_clean)

    # Check for zero vector
    if not np.any(doc.vector):
        return -1

    # Scale embedding safely
    try:
        command_scaled = scaler.transform(doc.vector.reshape(1, -1))
    except ValueError as e:
        print(f"⚠️ Scaling error: {e}")
        return -1

    # Predict intent number
    try:
        intent_number = int(stack_clf.predict(command_scaled)[0])
        return intent_number
    except Exception as e:
        print(f"⚠️ Prediction error: {e}")
        return -1


# 5️⃣ Function to execute the predicted intent
def execute_intent(intent: int):
    """Executes a system or web action based on the intent number."""
    try:
        if intent == GET_TIME:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            print("⏰ Current Time:", current_time)
            text_to_speech(f"The current time is {current_time}")

        elif intent == SEARCH_GOOGLE:
            text_to_speech("What do you want to search on Google?")
            query = speech_to_text()
            if query:
                webbrowser.open(f"https://www.google.com/search?q={query}")
                text_to_speech(f"Searching Google for {query}")

        elif intent == SEARCH_YOUTUBE:
            text_to_speech("What do you want to search on YouTube?")
            query = speech_to_text()
            if query:
                webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
                text_to_speech(f"Searching YouTube for {query}")

        elif intent == OPEN_NOTEPAD:
            os.system("notepad.exe")
            text_to_speech("Opening Notepad")

        elif intent == OPEN_CALCULATOR:
            os.system("calc.exe")
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
            if os.system("spotify.exe") != 0:
                webbrowser.open("https://open.spotify.com/")
                text_to_speech("Opening Spotify in browser")
            else:
                text_to_speech("Opening Spotify")

        elif intent == EXIT_INTENT:
            text_to_speech("Goodbye! Shutting down.")
            print("👋 Exiting...")
            sys.exit(0)

        else:
            text_to_speech("Sorry, I don't know how to handle this command yet.")

    except Exception as e:
        print(f"⚠️ Error while executing intent: {e}")
        text_to_speech("Something went wrong while executing your command.")


# 6️⃣ Start voice assistant
if __name__ == "__main__":
    text_to_speech("Hello! I am your voice assistant. Listening for commands...")
    while True:
        try:
            command = speech_to_text()
            if command:
                print(f"🎤 You said: {command}")
                intent = find_intent(command)
                print(f"🔍 Identified Intent: {intent}")
                execute_intent(intent)
            else:
                text_to_speech("I didn't catch that. Please say it again.")
        except KeyboardInterrupt:
            text_to_speech("Goodbye! Exiting now.")
            print("👋 Keyboard interrupt detected, shutting down.")
            sys.exit(0)
        except Exception as e:
            print(f"⚠️ Unexpected error: {e}")
            text_to_speech("An error occurred. Please try again.")
