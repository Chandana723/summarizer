import streamlit as st
import pyttsx3
import speech_recognition as sr
import webbrowser
import wikipedia
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube

# Initialize pyttsx3 for text-to-speech
def speak(audio):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(audio)
    engine.runAndWait()

# Initialize speech recognition for voice commands
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

# Function to greet the user
def Hello():
    speak("hello sir I am your video transcript summarizer.How can i help you today?")
    # Set the flag to indicate Hello() has been executed
    with open("hello_executed.txt", "w") as f:
        f.write("1")

# Check if Hello() has been executed before
def check_hello_executed():
    return os.path.isfile("hello_executed.txt")

# Function to extract transcript details from YouTube video
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]
        return transcript
    except Exception as e:
        raise e

# Function to generate summary based on prompt from Google Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Streamlit interface
def main():
    load_dotenv()  # Load environment variables
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Configure Google API

    st.title("Video Transcript Summarizer with Chatbot")

    # Check if Hello() function has been executed before
    if not check_hello_executed():
        Hello()  # Call Hello() function here

    # Chatbot
    query = st.text_input("You can also type your commands here:")
    if query:
        if "open google" in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")
        elif "How are you" in query:
            speak("I am good, how about you?")
        elif "open youtube" in query:
            speak("Opening Youtube")
            webbrowser.open("https://www.youtube.com/")
        elif "bye" in query:
            speak("Bye. Check out for the detailed notes.")

    youtube_link = st.text_input("Enter YouTube video link: ")
    if youtube_link:
        video_id = youtube_link.split("=")[1]
        st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

    if st.button("Get Detailed Notes"):
        transcript_text = extract_transcript_details(youtube_link)

        if transcript_text:
            prompt = "you are youtube video summarizer. you will be taking the transcript text and provide 10 important questions . The transcript text will be appended here: "
            summary = generate_gemini_content(transcript_text, prompt)
            st.markdown("## Detailed Notes:")
            st.write(summary)
            speak(summary)
            speak("Thankyou!")

if __name__ == "__main__":
    main()


