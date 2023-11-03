import snowboydecoder
import speech_recognition as sr
from gtts import gTTS
import os

# Replace 'your-hotword-model.pmdl' with your custom Snowboy model.
HOTWORD_MODEL = 'your-hotword-model.pmdl'

def say(text):
    tts = gTTS(text)
    tts.save('output.mp3')
    os.system('mpg123 -q output.mp3')

def handle_command(command):
    if 'joke' in command:
        say("Why don't scientists trust atoms? Because they make up everything!")
    elif 'morning' in command:
        say("Good morning! How can I assist you today?")
    elif 'fact' in command:
        say(" Sloths can hold their breath longer than dolphins")
    elif 'human' in command:
        say("Here is a Fun Fact about humans! Did you know humans can’t walk in a straight line without looking at something")
    elif 'boeing' in command:
        say("I know a Fun fact about Boeing airplanes did you know that they used potatoes to test their in-flight Wi-Fi! thats right Potatoes")
    elif 'skunk'
        say("eww skunks thoes stinky creatures did you know that A skunk's smell can be detected by a human a mile away")
    elif 'exit' in command:
        say("Goodbye!")
        exit()
    else:
        say("I didn't understand your command. Please try again.")

def hotword_detected_callback():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        print(f"You said: {command}")
        handle_command(command.lower())
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
    except sr.RequestError as e:
        print(f"Request error: {e}")

if __name__ == '__main__':
    detector = snowboydecoder.HotwordDetector(HOTWORD_MODEL, sensitivity=0.5)
    print("Listening for the hotword...")
    detector.start(detected_callback=hotword_detected_callback, sleep_time=0.03)
