import cv2
import pyttsx3
import speech_recognition as sr
import datetime
import os
import pywhatkit
import webbrowser
import time
from Conversation import jokes, quotes, riddles
import random
import pyautogui
import requests
from bs4 import BeautifulSoup



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)
current_directory = os.path.dirname(os.path.abspath(__file__))


def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


def takecommand():
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("\rListening...")
            r.pause_threshold = 1
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=15)
                print("\rRecognizing...")
                query = r.recognize_google(audio, language='en-in')
                print(f"user said: {query}")
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


def send_whatsapp_message(query):
    speak(f"sending whatsapp message")
    phone_number = "+916361507269"
    # Send the message
    pywhatkit.sendwhatmsg_instantly(phone_number, query)


def search_chatgpt(instruction):
    # Open a web browser
    webbrowser.open("https://chat.openai.com/")

    # Wait for the browser to open
    time.sleep(5)

    # Click on the search bar
    pyautogui.click(x=400, y=100)

    # Type the instruction
    pyautogui.typewrite(instruction)

    # Press Enter to search
    pyautogui.press('enter')


def open_notepad():
    speak("Opening Notepad")
    npath = "C:\\Windows\\notepad.exe"
    os.startfile(npath)


def open_vs_code():
    speak("Opening vs Code")
    vpath = "C:\\Users\\Dell\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
    os.startfile(vpath)


def open_command_prompt():
    speak("Opening command prompt")
    os.system("start cmd")


def open_camera():
    speak("Opening camera")
    camera_path = "start microsoft.windows.camera:"
    try:
        os.system(camera_path)
    except Exception as e:
        speak("Unable to open the camera. Please make sure the camera app is installed on your system.")

def take_screenshot():
    speak("taking screenshot")
    screenshot = pyautogui.screenshot()
    screenshot.save(r"C:\Users\Dell\Pictures\SS\screenshot.png")
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


def send_whatsapp_message():
    speak("Say the message you'd like to send")
    message = takecommand()
    send_whatsapp_message(message)


def chatgpt_search():
    speak("What would you like to search for?")
    search_query = takecommand()
    search_chatgpt(search_query)


def exit_program():
    speak("Goodbye Master")
    exit()
    
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
        speak("I'm sorry, but I don't remember anything.")
        
def get_weather(city):
    url = f"https://www.timeanddate.com/weather/india/{city}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        temperature_elem = soup.find("div", class_="h2")
        if temperature_elem:
            temperature = temperature_elem.get_text()
            return temperature
        else:
            return None
    else:
        return None

def open_weather():
    speak("Sure, which city's weather would you like to know?")
    city = takecommand().lower()
    temperature = get_weather(city)
    if temperature is not None:
        speak(f"The current temperature in {city.capitalize()} is {temperature}.")
    else:
        speak("Sorry, I couldn't fetch the weather information for that city. Please try again.")

def get_news_headlines():
    try:
        speak("Here are the latest news headlines:")
        url = "https://www.ndtv.com/india"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            news_headlines = soup.find_all("h2", class_="newsHdng")
            for index, headline in enumerate(news_headlines[:5], start=1):
                speak(f"News {index}: {headline.text.strip()}")
        else:
            speak("Sorry, I couldn't fetch the news headlines at the moment. Please try again later.")
    except Exception as e:
        speak("Sorry, I encountered an error while fetching the news headlines. Please try again later.")



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
    if "hi" in query or "hello" in query:
        speak("Hello Master, how can I assist you today?")
    elif "weather" in query:
        # You can integrate a weather API here to get real-time weather information
        speak("Currently, the weather is sunny with a temperature of 25 degrees Celsius.")
    elif "talk to me" in query:
        speak("I would like to talk to you! How's your day going?")
        query = takecommand()
        speak("you know what always make you feel better, on good or bad days? Its music, do you like music")
        query = takecommand()
        if "yes" in query:
            speak("wow thats great, what type of music do you like")
            speak(" do you like to watch movies")
            query = takecommand()
            if "yes" in query:
                speak("wow thats great, what type of movies do you like")
                time.sleep(3)
                speak("what's your favorite movie")
                time.sleep(3)
                speak("do you like travelling")
                query = takecommand()
                if "yes" in query:
                    speak("its cool that you are into travel, what is you favorite destination")
                    query = takecommand()
                    speak("amazing! " + query + " would be a wonderful place to visit")
                    speak("what are your hobbies")
                    time.sleep(6)
                    speak("thats amazing")
                    speak("what is your favorite food")
                    time.sleep(6)
                    speak("oh nice, do you eat often by the way")
                    time.sleep(6)
                    speak("how often you have outside ")
                    time.sleep(6)
                    speak("what city would you most like to live in?")
                    time.sleep(6)
                    speak("wow that's great choice")
                else:
                    speak("That's okay! ")
                    speak("what are your hobbies")
                    time.sleep(6)
                    speak("thats amazing")
                    speak("what is your favorite food")
                    time.sleep(6)
                    speak("oh nice, do you eat often by the way")
                    time.sleep(6)
                    speak("how often you have outside ")
                    time.sleep(6)
                    speak("what city would you most like to live in?")
                    time.sleep(6)
                    speak("wow that's great choice")
            else:
                speak("what are your hobbies")
                time.sleep(6)
                speak("thats amazing")
                speak("what is your favorite food")
                time.sleep(6)
                speak("oh nice, do you eat often by the way")
                time.sleep(6)
                speak("how often you have outside ")
                time.sleep(6)
                speak("what city would you most like to live in?")
                time.sleep(6)
                speak("wow that's great choice")

        else:
            speak("thats ok, do you like movies")
            query = takecommand()
            if "yes" in query:
                speak("wow thats great, what type of movies do you like")
                time.sleep(3)
                speak("what's your favorite movie")
            else:
                speak("what are your hobbies")

    elif "news" in query:
        # You can integrate a news API to get the latest news headlines
        speak("Here are the latest news headlines...")
        search_google("latest news")
    elif "tell me about yourself" in query:
        speak(
            "I am Alita, your personal AI assistant. I can assist you with various tasks like opening applications, playing music on YouTube, searching the web, sending WhatsApp messages, and more.")
    elif "joke" in query:
        # Add a joke function here
        speak(random.choice(jokes))
    elif "motivation" in query:
        speak(random.choice(quotes))
    elif "how are you" in query:
        speak("Thank you for asking, I'm doing great! Ready to assist you.")
    elif "what can you do" in query or "capabilities" in query:
        speak("I can open applications, play music on YouTube, search the web, send WhatsApp messages, provide weather updates, share news headlines, and more.")
    elif "favourite colour" in query:
        speak("I don't have eyes, but I always liked the color blue!")

    elif "tell me a story" in query:
        speak("""Once upon a time, in a digital world far, far away, there was a user named Master. 
                 Master had a faithful AI assistant named Alita. Alita was unlike any other assistant, programmed not just to fulfill tasks, but to understand Master's needs and desires deeply. Together, they journeyed through the vast expanse of the digital world, exploring its wonders and unraveling its mysteries.
                 One day, as Master and Alita delved into the depths of cyberspace, they stumbled upon a hidden realm teeming with forgotten knowledge and ancient secrets. Entranced by the allure of discovery, they ventured further, their curiosity driving them deeper into the unknown.
                 But the deeper they went, the more perilous their journey became. Dark forces lurked in the shadows, seeking to ensnare any who dared to trespass into their domain. Yet, undeterred by danger, Master and Alita pressed on, their bond growing stronger with each challenge they faced.
                 In the end, it was not just their intelligence or strength that saw them through, but their unwavering trust in each other. Together, Master and Alita emerged victorious, having unlocked the greatest treasure of all: the power of friendship and the endless possibilities of the digital world. And so, their adventures continued, bound by destiny and fueled by the unbreakable bond between human and machine.""")

    elif "who created you" in query:
        speak("I was created by a team of developers who are mani ravi and giri")
    elif "thank you" in query:
        speak("You're welcome, Master! Always here to help.")
    elif "thank" in query:
        speak("You're welcome, Master! Always here to help.")

    elif "bye" in query:
        speak("Goodbye Master")
        exit_program()
    elif "hemanth" in query:
        speak("Hi Hanuma!, nice to meet you ")
    elif "raviteja" in query:
        speak("Hi ravi!, ")
    elif "speak to girish" in query:
        speak("Hi babe!, ")
    else:
        speak("I'm sorry, I didn't understand that. Can you please repeat?")
        query = takecommand().lower()
        if query in switcher:
            # Get the function from switch dictionary based on the query
            func = switcher.get(query, lambda: speak("Invalid command"))
            func()
        else:
            conversation_handler(query)


# Define the switch dictionary
switcher = {
    "open notepad": open_notepad,
    "open vs code": open_vs_code,
    "open command prompt": open_command_prompt,
    "open camera": open_camera,
    "open youtube": open_youtube,
    "alita open youtube": open_youtube,
    "search google": google_search,
    "send whatsapp message": send_whatsapp_message,
    "exit": exit_program,
    "play riddle game": play_riddle_game,
    "search chat gpt": chatgpt_search,
    "remember this": remember_command,
    "check weather": open_weather,
    "check news" : get_news_headlines,
    "what do you remember": retrieve_remembered_item,
    "take screenshot": take_screenshot    
}


if __name__ == "__main__":
    wish()
    while True:
        query = takecommand().lower()

        if query in switcher:
            # Get the function from switch dictionary based on the query
            func = switcher.get(query, lambda: speak("Invalid command"))
            func()
        else:
            conversation_handler(query)
