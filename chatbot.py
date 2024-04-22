import pyttsx3
import speech_recognition as sr
import webbrowser
import wikipedia

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening')
        r.pause_threshold = 0.7
        audio = r.listen(source)
        try:
            print("Recognizing")
            Query = r.recognize_google(audio, language='en')
            print("the command is printed=", Query)
        except Exception as e:
            print(e)
            print("Say that again sir/mam")
            return "None"
        return Query

def speak(audio):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(audio)
    engine.runAndWait()

def Hello():
    speak("hello sir I am your video summarizer. Tell me which video you wanted to take help")

def Take_query():
    Hello()
    while True:
        query = takeCommand().lower()
        if "open google" in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")
        elif "open youtube" in query:
            speak("Opening Youtube")
            webbrowser.open("https://www.youtube.com/")
        elif "bye" in query:
            speak("Bye. Check Out for the detailed notes")
            break

if __name__ == '__main__':
    Take_query()