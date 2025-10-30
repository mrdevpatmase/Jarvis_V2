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

# 2️⃣ Load spaCy model
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
EXIT_INTENT = 9

# 4️⃣ Intent prediction
def find_intent(command: str) -> int:
    if not command.strip():
        return -1

    command_clean = " ".join(
        [word for word in command.lower().split() if word not in stopwords]
    )
    doc = nlp(command_clean)

    if not np.any(doc.vector):
        return -1

    try:
        command_scaled = scaler.transform(doc.vector.reshape(1, -1))
        return int(stack_clf.predict(command_scaled)[0])
    except Exception as e:
        print(f"⚠️ Prediction error: {e}")
        return -1

# 5️⃣ Web-based Intent Execution
# def execute_intent(intent: int):
    """Performs web-based actions (Render-compatible)."""
    try:
        if intent == GET_TIME:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"⏰ Current Time: {current_time}")
            text_to_speech(f"The current time is {current_time}")

        elif intent == SEARCH_GOOGLE:
            webbrowser.open("https://www.google.com/")
            text_to_speech("Opening Google")

        elif intent == SEARCH_YOUTUBE:
            webbrowser.open("https://www.youtube.com/")
            text_to_speech("Opening YouTube")

        elif intent == OPEN_NOTEPAD:
            webbrowser.open("https://editpad.org/")
            text_to_speech("Opening Online Notepad")

        elif intent == OPEN_CALCULATOR:
            webbrowser.open("https://www.google.com/search?q=online+calculator")
            text_to_speech("Opening Online Calculator")

        elif intent == OPEN_WHATSAPP:
            webbrowser.open("https://web.whatsapp.com/")
            text_to_speech("Opening WhatsApp Web")

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
            text_to_speech("Goodbye! Shutting down.")
            print("👋 Exiting...")
            sys.exit(0)

        else:
            text_to_speech("Sorry, I don't know this command yet.")

    except Exception as e:
        print(f"⚠️ Error while executing intent: {e}")
        text_to_speech("Something went wrong while executing your command.")


def execute_intent(intent: int):
    """Executes a web-based action based on the intent number."""
    try:
        if intent == GET_TIME:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            return f"The current time is {current_time}"

        elif intent == SEARCH_GOOGLE:
            return "Opening Google... <a href='https://www.google.com/' target='_blank'>Click here</a>"

        elif intent == SEARCH_YOUTUBE:
            return "Opening YouTube... <a href='https://www.youtube.com/' target='_blank'>Click here</a>"

        elif intent == OPEN_WHATSAPP:
            return "Opening WhatsApp Web... <a href='https://web.whatsapp.com/' target='_blank'>Click here</a>"

        elif intent == OPEN_LINKEDIN:
            return "Opening LinkedIn... <a href='https://www.linkedin.com/' target='_blank'>Click here</a>"

        elif intent == OPEN_GITHUB:
            return "Opening GitHub... <a href='https://github.com/' target='_blank'>Click here</a>"

        elif intent == OPEN_SPOTIFY:
            return "Opening Spotify... <a href='https://open.spotify.com/' target='_blank'>Click here</a>"

        elif intent == EXIT_INTENT:
            return "Goodbye! Have a great day 👋"

        else:
            return "Sorry, I don’t know how to handle that command yet."

    except Exception as e:
        print(f"⚠️ Error while executing intent: {e}")
        return "Something went wrong while processing your command."


# 6️⃣ Start (Voice or Text Mode)
if __name__ == "__main__":
    text_to_speech("Hello! I am your Jarvis web assistant. Listening for commands...")
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
            print("👋 Shutting down.")
            sys.exit(0)
        except Exception as e:
            print(f"⚠️ Unexpected error: {e}")
            text_to_speech("An error occurred. Please try again.")
