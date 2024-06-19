
import pyttsx3
import requests
import speech_recognition as sr
import keyboard
import os
import subprocess as sp
import imdb
from datetime import datetime
from decouple import config
from random import choice
from conv import random_text


from online import find_my_ip,search_on_google,serch_on_wikipedia,youtube,send_email,get_news,weather_forecast

engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 1.5)
engine.setProperty('rate', 225)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

USER = config('USER')
HOSTNAME = config('BOT')

def greet_me():
    hour = datetime.now().hour
    if (hour<=6) and (hour<=12):
        speak(f'Good Morning {USER}')
    elif (hour>=12) and (hour<=16):
        speak(f'Good Afternoon {USER}')
    elif (hour>=16) and (hour<=19):
        speak(f'Good Evening {USER}')
    speak(f'I am  {HOSTNAME}. how may i assist you {USER}?')


listening = False
def start_listening():
    global listening
    listening = True
    print(' Started Listening...')

def pause_listening():
    global listening
    listening = False
    print("Stopping Listening...")


keyboard.add_hotkey('ctrl+alt+k', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)



def take_command(none='None'):
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold=1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        queri=r.recognize_google(audio,language='en-in')
        print(queri)
        if not 'stop' in queri or 'exit' in queri:
            speak(choice(random_text))
        else:
            hour=datetime.now().hour
            if hour >=21 and hour <6:
                speak(f'Good Night{USER} , take care')
            else:
                speak('Have a good day')
            exit()
    except Exception:
        speak("Sorry I couldn't understand. can you please repeat that?")
        queri= none
    return queri

def speak(text):
    engine.say(text)
    engine.runAndWait()


if __name__ == '__main__':
    greet_me()
while True:
    if listening:
        query = take_command().lower()
        if "how are you" in query:
            speak("I'm absolutely fine sir . What about you?")
        elif "open command prompt" in query:
            speak("Opening Command Prompt")
            os.system("start cmd")
        elif 'open camera' in query:
            speak("Opening Camera")
            sp.run('start microsoft.windows.camera',shell=True)
        elif "open notepad" in query:
            speak("Opening Notepad for you sir")
            notepad_path="C:\\Windows\\notepad.exe"
            os.startfile(notepad_path)
        elif "open chrome" in query:
            speak("Opening Chrome for you sir")
            chrome_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            os.startfile(chrome_path)
        elif " ip address" in query:
            ip_address= find_my_ip()
            speak(f"Your IP Address is {ip_address}")
            print('your IP Address is {}'.format(ip_address))
        elif "open youtube" in query:
            speak("What do you want to play on YouTube sir")
            video=take_command().lower()
            youtube(video)
        elif "open google" in query:
            speak("What do you want to search on Google sir")
            query=take_command().lower()
            search_on_google(query)
        elif "open wikipedia" in query:
            speak("What do you want to search on Wikipedia sir")
            search=take_command().lower()
            results= serch_on_wikipedia(search)
            speak(f"According to Wikipedia is {results}")
            speak("Im printing on terminal")
            print(results)

        elif "send email" in query:
            speak("On what email address do you want to send sir? please enter in the terminal")
            receiver_add=input("Email Address: ")
            speak("What should be the subject of the email sir")
            subject=take_command().capitalize()
            speak("what is the message?")
            message=take_command().capitalize()
            if send_email(receiver_add,subject,message):
                speak("Ive sent the email to the mentioned mail ID sir")
                print("Email has been sent")
            else:
                speak("Something went wrong. Please try again")
        elif "give me news" in query:
            speak("Im reading out the latest news of today sir")
            speak(get_news())
            speak("Im printing on terminal sir")
            print(*get_news(),sep='\n')
        elif "give me weather" in query:
            ip_address = find_my_ip()
            speak("Tell me the name of your city")
            city = input("Enter name of your city:")
            speak(f"Getting Weather report of your city {city}")
            weather, temp, feels_like = weather_forecast(city)
            speak(f"The current temperature is {temp}, but it feels like {feels_like}")
            speak(f"Also the weather report talks about {weather}")
            speak("For your convenience,I'm printing on terminal")
            print(f"Description: {weather}\nTemperature: {temp}\nFeels like: {feels_like}")

        elif "movie review" in query:
            movies_db=imdb.IMDb()
            speak("Please tell me the movie name")
            text=take_command()
            movies=movies_db.search_movie(text)
            speak(f"Searching for {text}")
            speak("I found these")
            for movie in movies:
                title=movie['title']
                year=movie['year']
                speak(f"{title} - {year}")
                info=movie.getID()
                movie_info=movies_db.get_movie(info)
                rating= movie_info['rating']
                cast=movie_info['cast']
                actor=cast[0:3]
                plot=movie_info.get('plot outline','plot summary not available')
                speak(f"{title} was released in {year} has imdb ratings of {rating}. It has cast of {actor}.The plot summary of movie is {plot}")
                print(
                    f"{title} was released in {year} has imdb ratings of {rating}. It has cast of {actor}.The plot summary of movie is {plot}")