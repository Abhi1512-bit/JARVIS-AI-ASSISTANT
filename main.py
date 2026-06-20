import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize components
recognizer = sr.Recognizer()
engine = pyttsx3.init()

client = genai.Client(api_key=GEMINI_API_KEY)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def ask_ai(question):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=question
    )
    return response.text

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")

    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")

    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
        )

        data = r.json()

        titles = [
            article.get("title", "No Title")
            for article in data.get("articles", [])
        ]

        speak("Here are the top headlines")

        for title in titles[:5]:
            print(title)
            speak(title)

    else:
        answer = ask_ai(c)
        print(answer)
        speak(answer)

if __name__ == "__main__":
    speak("Initializing Jarvis")

    while True:
        r = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1)
                print("Listening for wake word...")

                audio = r.listen(
                    source,
                    timeout=2,
                    phrase_time_limit=1
                )

                word = r.recognize_google(audio)

                if word.lower() == "jarvis":
                    speak("Yes Sir")

                    with sr.Microphone() as source:
                        print("Listening for command...")
                        audio = r.listen(source)

                    command = r.recognize_google(audio)
                    processCommand(command)

        except Exception as e:
            print(f"Error: {e}")