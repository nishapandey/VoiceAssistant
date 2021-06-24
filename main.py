from flask import Flask
import speech_recognition as sr
import webbrowser
import time
import playsound
import os
import random
from gtts import gTTS
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

from time import ctime

app = Flask(__name__)
r = sr.Recognizer()
# Install chrome driver
# Login to linkedin or navigate jobs with voice commands
# TODO: remove credentials to improvise
def linkedinLogin( ):
    driver = webdriver.Chrome("//usr/local/bin/chromedriver")
    driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
    user_textbox = "pandeyn14@students.ecu.edu"
    password_textbox = ""
    if not user_textbox or not password_textbox :
        speak('please enter your credentials')
    else:
        user = driver.find_element_by_id("username")
        user.send_keys(user_textbox)
        user.send_keys(Keys.TAB)
        password = driver.find_element_by_id("password")
        password.send_keys(password_textbox)
        user.send_keys(Keys.TAB)
        # future enhancement - add code for incorrect credentials
        # add use case for sign up
        login_btn = driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button')
        login_btn.submit()

# navigate jobs
def navigate():
    driver = webdriver.Chrome("//usr/local/bin/chromedriver")
    driver.get("https://www.linkedin.com/jobs/")


@app.route('/')
def record_audio(ask = False):

    with sr.Microphone() as source:
        if ask:
            speak(ask)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)

        except sr.UnknownValueError:
            speak( 'Sorry i did not get that')
        except sr.RequestError:
            speak ('Sorry, my speech service is down')
    return voice_data  # Press ⌘F8 to toggle the breakpoint.

def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 10000000)
    audio_file = 'audio-'+str(r) +'.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)


#intents
def respond(voice_data):
    print(voice_data)

    if"what's your name" in voice_data:
        speak ('My name is Emma')

    if'what time is it' in voice_data:
        speak(ctime())

    if'search' in voice_data:
        search = record_audio('What do you want to search for?')
        url = 'https://google.com/search?q='+search
        webbrowser.get().open(url)
        speak('Here is what i found for '+search)

    if 'find location' in voice_data:
        search = record_audio('What is the location?')
        url = 'https://google.nl/maps/place/' + search +'/&amp;'
        webbrowser.get().open(url)

    if 'login' in voice_data:
        linkedinLogin()
        speak('you have arrived')

    if 'navigate jobs' in voice_data:
        navigate()

    if 'exit' in voice_data:
        speak('Exiting voice assistant' )
        exit()


sleep = 2
time.sleep(sleep)

speak('Hi,how can i help you?')

while(sleep):
    voice_data = record_audio();
    if not voice_data:
        time.sleep(sleep)
    else:
        respond(voice_data)

app.run(port=5000, debug=True)




