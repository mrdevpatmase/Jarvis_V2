import speech_recognition as sr
import pyttsx3


def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio)
        print(f"🎤 You said: {query}")
        return query
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        text_to_speech("Sorry, I didn't catch that. Please say it again.")
        return None
    except sr.RequestError:
        print("⚠️ Could not request results. Check your internet connection.")
        text_to_speech("I am having trouble connecting to the internet.")
        return None


def text_to_speech(info):
    engine = pyttsx3.init()
    engine.say(info)
    engine.runAndWait()
