import pyttsx3
import requests
import speech_recognition as sr
import datetime
import os
import cv2
import pywhatkit
import webbrowser
import time
from bs4 import BeautifulSoup
from Conversation import jokes, quotes, riddles
import  random
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math
from dotenv import load_dotenv
load_dotenv('.env')
import google.generativeai as genai


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 200)


def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def wait_until_alita():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for 'Alita'...")
        while True:
            audio = r.listen(source)
            try:
                query = r.recognize_google(audio, language='en-in')
                print(f"user said: {query}")
                if "alita" in query.lower():
                    print("Alita detected!")
                    return True
            except sr.UnknownValueError:
                print("Sorry, I didn't catch that. Listening...")
            except sr.RequestError:
                print("Sorry, I'm having trouble processing your request. Listening...")

def takecommand():
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=15)
                print("Recognizing...")
                query = r.recognize_google(audio, language='en-in')
                print(f"user said: {query}")

                if "wait" in query.lower():
                    speak("Waiting for your command...")
                    wait_until_alita()
                    speak("Resuming...")
                    continue

                if "calculate" in query.lower():
                    expression = query.lower().split("calculate", 1)[-1].strip()
                    calculate_math_expression(expression)
                    continue
                return query.lower()
            except sr.WaitTimeoutError:
                speak("Listening timed out. Please say something or say 'exit' to quit.")
                continue
            except Exception as e:
                speak("Say that again please...")
                continue


def wish():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning Master")
    elif 12 <= hour < 18:
        speak("Good Afternoon Master")
    else:
        speak("Good Evening Master")
    speak("I'm Alita....Your Personal AI Assistant...Please tell me How can I help you")

def play_youtube(query):
    pywhatkit.playonyt(query)

def search_google(query):
    speak(f"Searching Google for {query}")
    url = f"https://www.google.com/search?q={'+'.join(query.split())}"
    webbrowser.open(url, new=2)
    time.sleep(2)
    speak("Here are the search results from Google. I hope you find them useful.")
    
def send_whatsapp_message_auto():
    speak("Whom do you want to send the message to?")
    recipient_name = takecommand()
    if recipient_name == "":
        return
    speak(f"Recipient's name is {recipient_name}")

    speak("What message do you want to send?")
    message = takecommand()
    if message == "":
        return
    speak(f"Message is: {message}")

    pyautogui.press('win')
    time.sleep(1)
    pyautogui.write('whatsapp', interval=0.1)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)

    pyautogui.click(x=350, y=150)
    time.sleep(1)

    pyautogui.write(recipient_name, interval=0.1)
    time.sleep(3)

    pyautogui.press('down')
    pyautogui.press('enter')
    time.sleep(3)

    pyautogui.write(message, interval=0.1)
    pyautogui.press('enter')


def search_chatgpt(instruction):
    webbrowser.open("https://chat.openai.com/")
    time.sleep(5)
    pyautogui.click(x=400, y=100)
    pyautogui.typewrite(instruction)
    pyautogui.press('enter')

def open_application(app_name):
    pyautogui.press('win')
    time.sleep(1)
    pyautogui.write(app_name, interval=0.1)
    pyautogui.press('enter')
    time.sleep(2)


# Weather API
def get_weather(city):
    api_key = os.getenv('WEATHER_API_KEY')
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': api_key, 'units': 'metric'}

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'main' in data and 'temp' in data['main'] and 'weather' in data and len(data['weather']) > 0:
            temperature = data['main']['temp']
            description = data['weather'][0]['description']
            return temperature, description
        else:
            return None, None
    else:
        return None, None


def increase_volume(increment):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = min(1.0, current_volume + increment)
    volume.SetMasterVolumeLevelScalar(new_volume, None)

def decrease_volume(decrement):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = max(0.0, current_volume - decrement)
    volume.SetMasterVolumeLevelScalar(new_volume, None)

# News API
def get_news_headlines():
    try:
        api_key = os.getenv("NEWS_API_KEY")
        speak("Here are the latest news headlines:")
        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            for index, article in enumerate(articles[:5], start=1):
                speak(f"News {index}: {article['title'].split(' - ')[0]}")
        else:
            speak("Sorry, I couldn't fetch the news headlines at the moment. Please try again later.")
    except Exception as e:
        speak("Sorry, I encountered an error while fetching the news headlines. Please try again later.")

def calculate_math_expression(expression):
    try:
        expression = expression.replace("x", "*")

        if "square root of" in expression:
            number = int(expression.split("square root of")[1])
            result = math.sqrt(number)
            speak(f"The square root of {number} is {result}")
        elif "cube root of" in expression:
            number = int(expression.split("cube root of")[1])
            result = number ** (1 / 3)
            speak(f"The cube root of {number} is {result}")
        else:
            result = eval(expression)
            speak(f"The result of {expression} is {result}")
    except Exception as e:
        speak("Sorry, I couldn't calculate that. Please provide a valid mathematical expression.")


def scroll_up():
    time.sleep(1)
    pyautogui.scroll(250)
    speak("scrolled up")

def scroll_down():
    time.sleep(1)
    pyautogui.scroll(-250)
    speak("scrolled down")

def click_left():
    speak("clicking left")
    pyautogui.press("left")

def click_right():
    speak("clicking right")
    pyautogui.press("right")

def click_up():
    speak("clicking up")
    pyautogui.press("up")

def click_down():
    speak("clicking down")
    pyautogui.press("down")

def click_enter():
    speak("clicking enter")
    pyautogui.press("enter")


def open_word():
    speak("Opening  word")
    open_application("word")

def open_powerpoint():
    speak("Opening  power point")
    open_application("powerpoint")

def open_excel():
    speak("Opening excel")
    open_application("excel")

def open_calender():
    speak("Opening calender")
    open_application("calender")

def open_calculator():
    speak("opening calculator")
    open_application("calculator")

def open_amazon_prime_video():
    speak("opening amazon prime video")
    open_application("prime video")
def open_netflix():
    speak("opening netflix")
    open_application("netflix")
def open_mail():
    speak("opening mail")
    open_application("mail")
def open_teams():
    speak("opening teams")
    open_application("teams")
def open_settings():
    speak("opening settings")
    open_application("settings")
def open_control_panel():
    speak("opening control panle")
    open_application("control panel")
def open_task_manager():
    speak("opening task manager")
    open_application("task manager")
def open_photos():
    speak("opening photos")
    open_application("photos")
def open_pycharm():
    speak("opening pycharm")
    open_application("pycharm")
def open_linkedin():
    speak("opening linkedin")
    open_application("linkedin")
def open_clock():
    speak("opening clock")
    open_application("clock")


if __name__ == "__main__":

    wish()
    while True:

        def volume_increase():
            increase_volume(0.2)
            speak("volume increased ")

        def volume_decrease():
            decrease_volume(0.2)
            speak("volume decreased")

        def show_desktop():
            pyautogui.hotkey('win', 'd')

        def close_application():
            pyautogui.hotkey('alt', 'f4')
            time.sleep(1)



        def minimize_application():
            screen_width, screen_height = pyautogui.size()
            minimize_button_x = screen_width -150  
            minimize_button_y = 10

            pyautogui.moveTo(minimize_button_x, minimize_button_y, duration=0.5)
            pyautogui.click()

        def press_space():
            pyautogui.press('space')

        def maximize_application():
            pyautogui.hotkey('win', 'up')


        def open_notepad():
            speak("Opening Notepad")
            open_application("notepad")


        def open_vs_code():
            speak("Opening vs Code")
            open_application("vs code")


        def open_command_prompt():
            speak("Opening command prompt")
            open_application("command prompt")


        def open_camera():
            speak("Opening camera")
            open_application("camera")

        def open_spotify():
            speak("opening spotify")
            open_application("soptify")


        def take_screenshot():
           speak("taking screenshot")
           screenshot = pyautogui.screenshot()
           screenshot.save(r"C:\Users\Dell\OneDrive\Pictures\Screenshots\screenshot.png")
           speak("screenshot saved")

        def open_youtube():
            speak("What would you like to play?")
            song_query = takecommand()
            speak(f"Playing {song_query} on YouTube")
            play_youtube(song_query)


        def google_search():
            speak("What would you like to search for?")
            search_query = takecommand()
            search_google(search_query)

        def chatgpt_search():
            speak("What would you like to search for?")
            search_query=takecommand()
            search_chatgpt(search_query)

        def exit_program():
            speak("Goodbye Master")
            exit()

        def get_city_weather():
            speak("Sure, which city's weather would you like to know?")
            city = takecommand().lower()
            temperature, description = get_weather(city)
            if temperature is not None and description is not None:
                temperature_formatted = f"{temperature}°C"
                speak(f"The current temperature in {city.capitalize()} is {temperature_formatted} with {description}.")
            else:
                speak("Sorry, I couldn't fetch the weather information for that city. Please try again.")


        current_directory = os.path.dirname(os.path.abspath(__file__))
        def remember_command():
            speak("What would you like me to remember?")
            item_to_remember = takecommand()
            remember_item(item_to_remember)


        remember_file = os.path.join(current_directory, "remembered_items.txt")


        def remember_item(item):
            speak(f"Sure, I'll remember that {item}.")
            with open(remember_file, "a") as file:
                file.write(item + "\n")


        def retrieve_remembered_item():
            try:
                with open(remember_file, "r") as file:
                    remembered_items = file.readlines()
                    if remembered_items:
                        speak("Here are the things I remember:")
                        for item in remembered_items:
                            speak(item.strip())
                    else:
                        speak("I'm sorry, but I don't remember anything.")
            except FileNotFoundError:
                speak("I'm sorry, but I don't remember anything.")


        def play_riddle_game():
            speak("Let's play a riddle game!")
            while True:
                attempts = 3
                riddle = random.choice(riddles)
                while attempts > 0:

                    speak(riddle["question"])
                    correct_answer = riddle["answer"]
                    user_answer = takecommand().lower()

                    if user_answer == correct_answer.lower():
                        speak("Congratulations! You got it right.")
                        break

                    elif user_answer == "exit":
                        speak("Exiting the riddle game.")
                        return

                    else:
                        speak("Sorry, that's incorrect.")
                        attempts -= 1
                        if attempts > 0:
                            speak(f"You have {attempts} attempts left. Here's the same riddle again.")
                            speak(riddle["question"])
                        else:
                            speak(f"Sorry, you've run out of attempts. The answer is {correct_answer}.")
                            break

                speak("Would you like to play another riddle?")
                choice = takecommand().lower()
                if choice == "no":
                    speak("Okay, let me know if you want to play again. Goodbye!")
                    return
                else:

                    play_riddle_game()
        
        def conversation_handler(query):
            gemini_api_key = os.getenv("GEMINI_API_KEY") 
            if gemini_api_key:
                genai.configure(api_key=gemini_api_key)
                model = genai.GenerativeModel(model_name='gemini-pro')
                response = model.generate_content(query)
                try:
                    generated_text = response._result.candidates[0].content.parts[0].text
                    speak(generated_text)
                except Exception as e:
                    speak("Sorry, I couldn't process your request at the moment. Please try again later.")  
            else:
                speak("Sorry, I couldn't process your request at the moment. Please try again later.")



        # Define the switch dictionary
        switcher = {
            "open notepad": open_notepad,
            "open vs code": open_vs_code,
            "open command prompt": open_command_prompt,
            "open camera": open_camera,
            "open youtube": open_youtube,
            "search google": google_search,
            "send whatsapp message": send_whatsapp_message_auto,
            "exit": exit_program,
            "play riddle game":play_riddle_game,
            "search chat gpt":chatgpt_search,
            "take screenshot":take_screenshot,
            "check weather": get_city_weather,
            "remember this": remember_command,
            "what do you remember": retrieve_remembered_item,
            "maximize":maximize_application,
            "minimize":minimize_application,
            "minimise":minimize_application,
            "close":close_application,
            "minimize all":show_desktop,
            "play":press_space,
            "pause pause":press_space,
            "pause":press_space,
            "space":press_space,
            "increase volume":volume_increase,
            "decrease volume":volume_decrease,
            "open spotify":open_spotify,
            "check news":get_news_headlines,
            "scroll up":scroll_up,
            "scroll down":scroll_down,
            "open word":open_word,
            "open power point ":open_powerpoint,
            "open excel":open_excel,
            "open calender":open_calender,
            "open calculator":open_calculator,
            "open amazon prime video":open_amazon_prime_video,
            "open netflix":open_netflix,
            "open email":open_mail,
            "open mail":open_mail,
            "open teams":open_teams,
            "open settings":open_settings,
            "open control panel":open_control_panel,
            "open task manager":open_task_manager,
            "open photos":open_photos,
            "open pie chart": open_pycharm,
            "open python": open_pycharm,
            "open clock":open_clock,
            "open linkedin":open_linkedin,
            "click left":click_left,
            "click right":click_right,
            "click up":click_up,
            "click down":click_down,
            "click enter":click_enter,

            "alita open notepad": open_notepad,
            "alita open vs code": open_vs_code,
            "alita open command prompt": open_command_prompt,
            "alita open camera": open_camera,
            "alita open youtube": open_youtube,
            "alita alita open youtube": open_youtube,
            "alita search google": google_search,
            "alita send whatsapp message": send_whatsapp_message_auto,
            "alita exit": exit_program,
            "alita play riddle game": play_riddle_game,
            "alita search chat gpt": chatgpt_search,
            "alita take screenshot": take_screenshot,
            "alita check weather": get_city_weather,
            "alita remember this": remember_command,
            "alita what do you remember": retrieve_remembered_item,
            "alita maximize": maximize_application,
            "alita minimize": minimize_application,
            "alita minimise": minimize_application,
            "alita close": close_application,
            "alita minimize all": show_desktop,
            "alita play": press_space,
            "alita pause pause": press_space,
            "alita pause": press_space,
            "alita space": press_space,
            "alita increase volume": volume_increase,
            "alita decrease volume": volume_decrease,
            "alita open spotify": open_spotify,
            "alita check news": get_news_headlines,
            "alita scroll up": scroll_up,
            "alita scroll down": scroll_down,
            "alita open word": open_word,
            "alita open power point ": open_powerpoint,
            "alita open excel": open_excel,
            "alita open calender": open_calender,
            "alita open calculator": open_calculator,
            "alita open amazon prime video": open_amazon_prime_video,
            "alita open netflix": open_netflix,
            "alita open email": open_mail,
            "alita open mail": open_mail,
            "alita open teams": open_teams,
            "alita open settings": open_settings,
            "alita open control panel": open_control_panel,
            "alita open task manager": open_task_manager,
            "alita open photos": open_photos,
            "alita open pie chart": open_pycharm,
            "alita open python":open_pycharm,
            "alita open clock": open_clock,
            "alita open linkedin": open_linkedin,
            "alita click left": click_left,
            "alita click right": click_right,
            "alita click up": click_up,
            "alita click down": click_down,
            "alita click enter": click_enter

        }


        query = takecommand().lower()


        if query in switcher:
            # Get the function from switch dictionary based on the query
            func = switcher.get(query, lambda: speak("Invalid command"))
            func()
        else:
            conversation_handler(query)



