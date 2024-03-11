import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import os
import wikipedia
import google.generativeai as genai
from giminiapi import api


chatStr = ""
def chat(query):
    global chatStr
    genai.configure(api_key=api)
    chatStr += f"User: {query}\n Jarvis: "
    generation_config = {
    "temperature": 0.6,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
    }
    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    ]

    model = genai.GenerativeModel(
        model_name="gemini-1.0-pro",
        generation_config=generation_config,
        safety_settings=safety_settings)

    convo = model.start_chat()
    convo.send_message(query)
    say(convo.last.text)
    chatStr += f"{convo.last.text}\n"
    return convo.last.text

def ai(prompt):
    genai.configure(api_key=api)
    text=f"Gemini response from Prompt : {prompt}\n********************************\n\n"
    generation_config = {
    "temperature": 0.6,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
    }
    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    ]

    model = genai.GenerativeModel(
        model_name="gemini-1.0-pro",
        generation_config=generation_config,
        safety_settings=safety_settings)

    convo = model.start_chat()
    convo.send_message(prompt)
    #print(convo.last.text)
    text += convo.last.text
    if not os.path.exists("Gemini"):
        os.mkdir("Gemini")

    with open(f"Gemini/{''.join(prompt.split('intelligence')[1:]).strip()}.txt","w") as f:
        f.write(text)

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)


def say(audio):
    print("Sophia : ",audio)
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        say("Good Morning!")
    elif hour >= 12 and hour < 18:
        say("Good Afternoon!")
    else:
        say("Good Evening!")  
    say("I am Sophia, I am your Virtual Assistant, How may i help you")

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        #r.pause_threshold = 0.8
        audio=r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio,language='en-in')
            print(f'User : {query}')
            return query
        except Exception as e:
            return "I didn't understand. Try Again! "

if __name__ == '__main__':
    wishMe()
    while True:

        print("Listening....")
        query=takeCommand()

        sites=[["youtube","https://youtube.com"],["wikipedia","https://wikipedia.com"],["google","https://google.com"],]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]}")
                webbrowser.open(site[1])
                exit()
        
        apps=[["chrome","C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"],["vs code","C:\\Users\\SHIVAM SINGH\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"]]
        for app in apps:
            if f"Open {app[0]}".lower() in query.lower():
                say(f"Opening {app[0]}")
                os.startfile(app[1])
                exit()

        if "the time" in query.lower():
            strfTime=datetime.datetime.now().strftime("%H:%M:%S")
            say(f"The time is {strfTime}")
        
        elif "exit".lower() in query.lower():
            say("Thanks For Using!!")
            print("Exiting....")
            exit()
        elif "Using Artificial intelligence".lower() in query.lower():
            say("processing")
            ai(prompt=query)
        
        elif 'wikipedia'.lower() in query.lower():
            say('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            say("According to Wikipedia")
            say(results)
        
        else:
            chat(query)