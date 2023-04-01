import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os

# Initialize the speech recognizer and text-to-speech engine
r = sr.Recognizer()
engine = pyttsx3.init()

# Define the voice assistant's voice properties
engine.setProperty('rate', 170)
engine.setProperty('volume', 1)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # You can change the voice ID as per your preference

# Define a function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Define a function to recognize speech
def recognize_speech():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Speak now...")
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that. Can you please repeat?")
        except sr.RequestError as e:
            speak("Sorry, I'm not able to process your request at the moment. Please try again later.")

# Define a function to set a reminder
def set_reminder():
    speak("What do you want me to remind you about?")
    reminder_text = recognize_speech()

    if reminder_text:
        speak("When do you want me to remind you?")
        reminder_time = recognize_speech()

        try:
            reminder_time = datetime.datetime.strptime(reminder_time, '%I:%M %p')
            now = datetime.datetime.now()

            if reminder_time < now:
                reminder_time += datetime.timedelta(days=1)

            time_diff = reminder_time - now
            seconds = time_diff.seconds

            speak(f"I will remind you about {reminder_text} in {seconds//3600} hours and {(seconds%3600)//60} minutes.")

            os.system(f'sleep {seconds} && say "Reminder: {reminder_text}" &')
        except ValueError:
            speak("Sorry, I couldn't understand the time. Please try again.")

# Define a function to create a to-do list
def create_todo():
    speak("What do you want to add to your to-do list?")
    todo_text = recognize_speech()

    if todo_text:
        with open('todo.txt', 'a') as f:
            f.write(f'{todo_text}\n')

        speak(f"Added {todo_text} to your to-do list.")

# Define a function to search the web
def search_web():
    speak("What do you want me to search for?")
    query = recognize_speech()

    if query:
        url = f"https://www.google.com/search?q={query}"
        webbrowser.get().open(url)
        speak(f"Here are the search results for {query}.")

# Define a function to greet the user
def greet():
    hour = datetime.datetime.now().hour

    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")

    speak("How can I assist you today?")

# Greet the user
greet()

# Start the voice assistant's main loop
while True:
    command = recognize_speech()

    if command:
        if 'reminder' in command:
            set_reminder()
        elif 'to-do' in command:
            create_todo()
        elif 'search' in command:
            search_web()
        elif 'exit' in command or 'stop' in command:
            speak("Goodbye!")
            break
        else:
            speak("Sorry, I couldn't understand that. Please try again.")