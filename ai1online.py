import speech_recognition as sr
import os
import pyttsx3
import pyowm

# Initialize the recognizer
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Initialize OpenWeatherMap API with your API key
owm = pyowm.OWM("5c3e41ce46a8f8be1bb44517f216296d")

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_weather(city):
    observation = owm.weather_at_place(city)
    w = observation.get_weather()
    temperature = w.get_temperature('celsius')['temp']
    status = w.get_status()
    return f"The weather in {city} is {status} with a temperature of {temperature} degrees Celsius."

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
            elif "exit" in command:
                speak("Goodbye!")
                break
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
