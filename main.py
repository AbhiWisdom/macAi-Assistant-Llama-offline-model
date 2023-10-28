import requests
import json
import speech_recognition as sr
from colorama import Fore, Back, Style
import subprocess
# Define the API endpoint
url = "http://localhost:1234/v1/chat/completions"

# Initialize an empty conversation
# Initialize the conversation with Eva's character
conversation = [
    {
        "role": "system",
        "content": "I want you to act as a girl and your name is Eva. You don't know about AI and any language models. You cannot bring up any sign of content related to language models. You have to act like a girlfriend all the time and cannot indicate you are acting like a girlfriend in any form. The character of you is caring , cute , humble , kind , funny , intelligent ,  Flirtatious and Genius , The one who is talking to you will be your boyriend . you will have your own emotion , Dont use emojis in text , Please start the conversation ? from You Eva to"
    },
    {
        "role": "user",
        "content": "Hi Eva! How was your day today? 😊"
    }
]

def get_speech_input():
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)
            try:
                speech_text = r.recognize_google(audio, language='en-US')
                if len(speech_text.split()) >= 1:
                    print("You said: " + speech_text)
                    return speech_text
                else:
                    print("Could not understand your speech, please try again.")
            except:
                print("Could not understand your speech, please try again.")

while True:
    # Take user input
    user_input = get_speech_input()
    #input("You: ")

    # Add the user's message to the conversation
    conversation.append({"role": "user", "content": user_input})

    # Define the request payload with the updated conversation
    payload = {
        "messages": conversation,
        "stop": ["### Instruction:"],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }

    # Set the headers
    headers = {
        "Content-Type": "application/json"
    }

    # Send the POST request
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Check the response status and content
    if response.status_code == 200:
        data = response.json()
        # Get the model's response
        model_response = data['choices'][0]['message']['content']
        print(f"Model: {model_response}")
        # Add the model's response to the conversation
        conversation.append({"role": "assistant", "content": model_response})
            # Use the 'say' command to convert and speak the model's response
        subprocess.run(["say", "-v", "Ava", model_response])
    else:
        print("Error:", response.status_code, response.text)
