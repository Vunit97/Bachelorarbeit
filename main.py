# necessary modules
import time
import pywhatkit as kit
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import subprocess
import pickle
import json
import requests
import wolframalpha
from ecapture import ecapture as ec
from deepface import DeepFace
from utils import extract_feature
from record_audio import record_audios

# import cv2: Just import it, when u use deepface to track ur emotions based on webcam

# Variable PHue Ip & Username to connect with PHue Lamps
bridge_ip = "192.168.178.146"
bridge_username = "xVscZVr4DTAkcnwLfUyRt3SFoafFFJeXSXVsrewL"

# Initialize Pyttsx3 (Text to Speech Library)
engine = pyttsx3.init()


# Text to Speech Library: Set up for changing the voice
def change_voice(engine, language, gender='VoiceGenderFemale'):
    for voice in engine.getProperty('voices'):
        if language in voice.languages and gender == voice.gender:
            engine.setProperty('voice', voice.id)
            return True

    raise RuntimeError("Language '{}' for gender '{}' not found".format(language, gender))


# Change Voice to female, and change the speed rate
change_voice(engine, 'en_US', 'VoiceGenderFemale')
engine.setProperty("rate", 170)

# Speak Function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Great Function
def welcome_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Hello Sir, Good Morning")
        print("Hello Sir, Good Morning")
    elif 12 <= hour < 18:
        speak("Hello Sir, Good Afternoon")
        print("Hello Sir, Good Afternoon")
    else:
        speak("Hello Sir, Good Evening")
        print("Hello Sir, Good Evening")

# Voice Command
def command_me():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening to...")
        listener.adjust_for_ambient_noise(source, duration=1)
        voice = listener.listen(source)

        try:
            voice_command = listener.recognize_google(voice, language='en-us')
            print(f"User said: {voice_command}\n")

        except Exception:
            speak("Excuse me, could you please repeat yourself")
            return "None"
        return voice_command


# Start of a Session with Loading and Greating
speak("Loading Friday - Your personal Assistant")
print("Loading Friday - Your personal Assistant")
welcome_me()

# Interaction Model
if __name__ == '__main__':

    speak("Is there anything i can do for you?")
    while True:
        voice_command = command_me().lower()

        # Open Browser
        if "open wikipedia" in voice_command:
            webbrowser.open_new_tab("https://www.wikipedia.de")
            speak("Wikipedia is open now.")
            time.sleep(4)
            speak("Is there anything else i can do for you?")

        elif "open gmail" in voice_command:
            webbrowser.open_new_tab("https://www.gmail.com")
            speak("Gmail is open now. ")
            time.sleep(4)
            speak("Is there anything else i can do for you?")

        # Searching Tools
        elif "open youtube" in voice_command:
            speak('What should i play on YouTube?')
            video_input = command_me().lower()
            kit.playonyt(video_input)
            speak("YouTube is open now.")
            time.sleep(4)
            speak("Is there anything else i can do for you?")

        elif "open google" in voice_command:
            speak('What should i search on Google?')
            search_input = command_me().lower()
            kit.search(search_input)
            speak("Google is open now. ")
            time.sleep(4)
            speak("Is there anything else i can do for you?")


        # Time Function
        elif "time" in voice_command:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime}")
            time.sleep(5)
            speak("Is there anything else i can do for you?")

        # Weather Function
        elif "weather" in voice_command:
            api_key = "c1ad43cb9ecb71cd603f115b43ea0e3e"
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            weather_url = "https://www.wetter.de/deutschland/wetter-"
            speak("Tell me the name of your city")
            city_name = command_me()
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            complete_weather_url = weather_url + city_name
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                current_temperature = ((x["main"]["temp"]) - 273.15)
                rounded_temperature = round(current_temperature)
                current_humidiy = x["main"]["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(" Temperature in centigrade unit is " + str(rounded_temperature))
                speak(" humidity in percentage is " + str(current_humidiy))
                speak(" Weather description  " + str(weather_description))
                print(" Temperature in centigrade unit = " +
                      str(rounded_temperature) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n Weather description = " +
                      str(weather_description))
                webbrowser.open_new_tab(complete_weather_url)

            else:
                speak("City not found")
            time.sleep(4)
            speak("Is there anything else i can do for you?")

        # News Letter Function
        elif 'news' in voice_command:
            query_params = {
                "source": "bbc-news",
                "sortBy": "top",
                "apiKey": "30ac6f82343c4554bd801cfcae63d411"
            }
            news_url = "https://newsapi.org/v1/articles"

            res = requests.get(news_url, params=query_params)
            open_bbc_page = res.json()

            article = open_bbc_page["articles"]

            results = []

            for ar in article:
                results.append(ar["title"])

            for i in range(len(results)):
                # printing all trending news
                print(i + 1, results[i])

            speak("Here are some of the top news. On the webpage of bbc you can read more about it.")
            webbrowser.open_new_tab("https://bbc.com")
            speak("First: " + results[0])
            speak("Second: " + results[1])
            speak("Third: " + results[2])
            time.sleep(3)
            speak("Is there anything else i can do for you?")

        # Questions
        elif "ask" in voice_command:
            speak('I can answer computational and geographical questions. So what question do you want to ask now?')
            question = command_me()
            app_id = "UWTH7L-2QYJ29PYPX"
            client = wolframalpha.Client("UWTH7L-2QYJ29PYPX")
            res = client.query(question)
            answer = next(res.results).text
            speak("The answer is: " + answer)
            print("The answer is: " + answer)
            time.sleep(3)
            speak("Is there anything else i can do for you?")

        # Light Function
        elif "turn on" in voice_command or "turn lights on" in voice_command or "lights on" in voice_command or "lamp on" in voice_command:

            payload = {"on": True}
            headers = {'content-type': 'application/json'}
            r = requests.put("https://" + bridge_ip + "/api/" + bridge_username + "/groups/1/action",
                             data=json.dumps(payload), headers=headers)
            speak("Your Lights are turning on.")
            time.sleep(3)
            speak("Is there anything else i can do for you?")

        elif "lights off" in voice_command or "lamp off" in voice_command:
            payload = {"on": False}
            headers = {'content-type': 'application/json'}
            r = requests.put("https://" + bridge_ip + "/api/" + bridge_username + "/groups/1/action",
                             data=json.dumps(payload), headers=headers)
            speak("Your Lights are turning off.")
            time.sleep(3)
            speak("Is there anything else i can do for you?")


        # Emotion Recognition per (face)
        elif "deepface" in voice_command or "deep face" in voice_command:

            speak(
                "I am gonna take a photo of you. To analyze how you feel based on your emotions. Make sure you are ready")
            ec.delay_imcapture(0, False, "img.jpg", 5)

            photo = DeepFace.analyze(img_path="img.jpg", actions=['emotion'])
            print("You are looking " + photo['dominant_emotion'])
            speak("You are looking " + photo['dominant_emotion'])

            if photo['dominant_emotion'] == "angry":
                speak(
                    "Perhaps you can let out all of your energy by hearing this rock playlist. Better days will come up. ")
                webbrowser.open_new_tab("https://www.youtube.com/watch?v=26nsBfLXwSQ")
            elif photo['dominant_emotion'] == "happy":
                speak("Accurate to your mood. I got an excellent playlist to live out your happiness")
                webbrowser.open_new_tab("https://www.youtube.com/watch?v=F-9s8pwo1jE")
            elif photo['dominant_emotion'] == "sad":
                speak(
                    "Maybe i can cheer up your mood with this playlist. It contains a lot of songs to boost your day.")
                webbrowser.open_new_tab("https://www.youtube.com/watch?v=APFMvzH1WEE")
            elif photo['dominant_emotion'] == "neutral":
                speak("This is a perfect setup to listen to this chill playlist.")
                webbrowser.open_new_tab("https://www.youtube.com/watch?v=iicfmXFALM8")

            time.sleep(3)
            speak("Is there anything else i can do for you?")

            """
            Old Version to track the emotion based on the webcam
            face_cascade_name = cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml'
            face_cascade = cv2.CascadeClassifier()
            if not face_cascade.load(cv2.samples.findFile(face_cascade_name)):
                print("Error loading xml file")
            cap = cv2.VideoCapture(0)

            while cap.isOpened():
                ret, frame = cap.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
                for (x, y, w, h) in faces:
                    roi_gray = gray[y:y + h, x:x + w]
                    roi_color = frame[y:y + h, x:x + w]
                    color = (0, 0, 255)
                    stroke = 2
                    end_cord_x = x + w
                    end_cord_y = y + h
                    cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)

                    analyze = DeepFace.analyze(frame, actions=["emotion"])
                    print("You are looking " + (analyze['dominant_emotion']))

                    cv2.imshow('frame', frame)
                    if cv2.waitKey(20) & 0xFF == ord('q'):
                        break
            """

        # SER Function
        elif "emotion recognition" in voice_command or "emotions" in voice_command:
            model = pickle.load(open("result/mlp_classifier.model", "rb"))
            speak("Tell me something. Maybe i can hear out how you feel...")
            print("Tell me something. Maybe i can hear out how you feel...")

            filename = "speech.wav"
            record_audios(filename)
            speech_features = extract_feature(filename, mfcc=True, mel=True, chroma=True).reshape(1, -1)
            result = model.predict(speech_features)[0]

            # Music recommendation
            speak("Let me think about it for a second")
            print("Let me think about it for a second")
            time.sleep(2)
            speak(
                f"From the volume, the pitch of your voice and several other components: I assume that you feel very {result}")
            print(
                "From the volume, the pitch of your voice and several other components: I assume that you feel very: " + result)

            if result == "angry":
                speak(
                    "Perhaps you can let out all of your energy by hearing this rock playlist. Better days will come up. ")
                webbrowser.open_new_tab("https://www.youtube.com/watch?v=26nsBfLXwSQ")
            elif result == "happy":
                speak("Accurate to your mood. I got an excellent playlist to live out your happiness")
                webbrowser.open_new_tab("https://www.youtube.com/watch?v=F-9s8pwo1jE")
            elif result == "sad":
                speak(
                    "Maybe i can cheer up your mood with this playlist. It contains a lot of songs to boost your day.")
                webbrowser.open_new_tab("https://www.youtube.com/watch?v=APFMvzH1WEE")
            elif result == "neutral":
                speak("This is a perfect setup to listen to this chill playlist.")
                webbrowser.open_new_tab("https://www.youtube.com/watch?v=dZzfbIhTe_s")

            time.sleep(5)
            speak("Is there anything else i can do for you?")

        # Close Voice Assistant
        if "goodbye" in voice_command or "ok bye" in voice_command or "stop" in voice_command:
            speak('Your personal assistant Friday is shutting down,Good bye')
            print('your personal assistant Friday is shutting down,Good bye')
            break

        # Shut PC Down
        elif 'turn off' in voice_command or 'log off' in voice_command or 'sign off' in voice_command:
            speak(
                "Ok , your pc will log off in 60 sec. If you are really sure about it, enter your password and make sure you exit from all applications")
            subprocess.call(["sudo", "-S", "shutdown", "-h", "+1"])
            break

time.sleep(3)
