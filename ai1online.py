import speech_recognition as sr
import os
import pyttsx3
import pyowm
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Initialize the recognizer
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Initialize OpenWeatherMap API with your API key
owm = pyowm.OWM("5c3e41ce46a8f8be1bb44517f216296d")

# Initialize Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="5db3f6d7b3c04429a4ad663987deba95",
                                               client_secret="08cacb3605674f2bbccc2fc5da73e490",
                                               redirect_uri="https://google.com",
                                               scope="user-library-read user-read-playback-state user-modify-playback-state"))

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_weather(city):
    observation = owm.weather_at_place(city)
    w = observation.get_weather()
    temperature = w.get_temperature('celsius')['temp']
    status = w.get_status()
    return f"The weather in {city} is {status} with a temperature of {temperature} degrees Celsius."

def play_spotify_track(track_name):
    results = sp.search(q=track_name, type="track")
    if results["tracks"]["items"]:
        track_uri = results["tracks"]["items"][0]["uri"]
        sp.start_playback(uris=[track_uri])
        speak(f"Playing {track_name} on Spotify.")
    else:
        speak(f"Sorry, I couldn't find the track {track_name} on Spotify.")

while True:
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print("You said: " + command)

            if "weather" in command:
                speak("Which city's weather would you like to know?")
                audio = recognizer.listen(source)
                city = recognizer.recognize_google(audio)
                weather_info = get_weather(city)
                speak(weather_info)
            elif "play music" in command:
                speak("What track would you like to play on Spotify?")
                audio = recognizer.listen(source)
                track_name = recognizer.recognize_google(audio)
                play_spotify_track(track_name)
            elif "exit" in command:
                speak("Goodbye!")
                break
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
