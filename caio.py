import pvporcupine
import os
import speech_recognition as sr
import pyttsx3
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from openai import wikipedia

# Initialize Porcupine with the custom wake word file
handle = pvporcupine.create(keywords=["fishy"])

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Initialize Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='5db3f6d7b3c04429a4ad663987deba95', client_secret='08cacb3605674f2bbccc2fc5da73e490', redirect_uri='https://google.com', scope='user-library-modify user-library-read user-read-playback-state user-modify-playback-state'))

def speak(text):
    engine.say(text)
    engine.runAndWait()

while True:
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # Detect the wake word "fishy" using Porcupine
    keyword_index = handle.process(audio)
    if keyword_index >= 0:
        print("Wake word detected.")
        
        # Implement logic to handle different voice commands
        command = recognizer.recognize_google(audio)
        print("You said: " + command)

        if "play music" in command:
            # Control Spotify to play music
            sp.start_playback()
            print("Playing music...")

        elif "pause music" in command:
            # Control Spotify to pause music
            sp.pause_playback()
            print("Pausing music...")

        elif "weather" in command:
            # Fetch and provide weather information (You would need to implement this part)
            print("Fetching weather...")

        elif "tell me about" in command:
            # Retrieve information from Wikipedia
            query = command.replace("tell me about", "").strip()
            try:
                result = wikipedia.summary(query, sentences=2)
                print("Wikipedia: " + result)
                speak(result)
            except wikipedia.exceptions.DisambiguationError as e:
                print("Multiple matches found. Please be more specific.")
            except wikipedia.exceptions.PageError as e:
                print("No matches found. Please refine your query.")

    else:
        print("Waiting for the wake word...")

# Close the Porcupine handle when done
handle.delete()
