import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from decouple import config

EMAIL = "kabilashkabi10@gmail.com"
PASSWORD = "cvkw ourf iymg ykjs"


def find_my_ip():
    ip_address = requests.get('https://api.ipify.org?format=json').json()
    return ip_address["ip"]


def serch_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results


def search_on_google(query):
    kit.search(query)


def youtube(video):
    kit.playonyt(video)


def send_email(receiver_add, subject, message):
    try:
        email = EmailMessage()
        email['To'] = receiver_add
        email['subject'] = subject
        email['from'] = EMAIL

        email.set_content(message)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True

    except Exception as e:
        print(e)
        return False


def get_news():
    news_headlines = []
    result = requests.get(
        'https://newsapi.org/v2/top-headlines?country=in&category=general&apiKey=ceda4f13ac564ffa879e2879696b1da9').json()
    articles = result['articles']
    for article in articles:
        news_headlines.append(article['title'])
    return news_headlines[:6]


def kelvin_to_celsius(temp_kelvin):
    return round(temp_kelvin - 273.15, 2)

def weather_forecast(city):
    res = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=ffbda1c820f988c0a0c59fb9a56d38d1").json()
    weather = res['weather'][0]['main']
    temp = kelvin_to_celsius(res['main']['temp'])
    feels_like = kelvin_to_celsius(res['main']['feels_like'])
    return weather, f'{temp}°C', f"{feels_like}°C"
