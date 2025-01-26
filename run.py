
import openai
import speech_recognition as sr
import pyttsx3
import json
import os
import sys
import subprocess
import requests
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

def load_config():
    config_path = "config.json"
    if not os.path.exists(config_path):
        print("Error: config.json not found.")
        exit()

    with open(config_path, "r") as json_file:
        return json.load(json_file)

config = load_config()

openai.api_key = config["keys"]["openai_api_key"]
openai.api_base = config["openai"]["api_base"]
openai_model = config["openai"]["model"]
max_tokens = config["openai"]["max_tokens"]
temperature = config["openai"]["temperature"]

recognizer = sr.Recognizer()
mic = sr.Microphone()
speech_timeout = config["speech_recognition"]["timeout"]
phrase_time_limit = config["speech_recognition"]["phrase_time_limit"]
language = config["speech_recognition"]["language"]

def print_blue(text): print("\033[94m" + text + "\033[0m")
def print_yellow(text): print("\033[93m" + text + "\033[0m")
def print_green(text): print("\033[92m" + text + "\033[0m")
def print_red(text): print("\033[91m" + text + "\033[0m")
def print_grey(text): print("\033[90m" + text + "\033[0m")

message_history_limit = config["assistant"]["message_history_limit"]
messages = [{"role": "system", "content": config["assistant"]["system_message"]}]

use_pyttsx3 = '--pyttsx3' in sys.argv
use_elevenlabs = '--elevenlabs' in sys.argv

if use_pyttsx3:
    tts_engine = pyttsx3.init()
    tts_engine.setProperty('rate', 150)

sprite_script_path = os.path.join(os.path.dirname(__file__), "gui.py")

sprite_process = subprocess.Popen(["python", sprite_script_path])

def elevenlabs_speak(text):
    try:
        elevenlabs_api_key = config["keys"]["elevenlabs_api_key"]
        voice_id = config["elevenlabs"]["voice_id"]
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": elevenlabs_api_key
        }
        data = {
            "text": text,
            "voice_settings": {
                "stability": 0.75,
                "similarity_boost": 0.75
            }
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
     
            audio_stream = BytesIO(response.content)
            audio = AudioSegment.from_file(audio_stream, format="mp3")
            play(audio)
        else:
            print_red(f"Error: ElevenLabs API returned {response.status_code}: {response.text}")
    except Exception as e:
        print_red(f"Error using ElevenLabs: {e}")

try:
    print_yellow("Chat with the assistant.")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print_blue("Microphone ready...")

        while True:
            print_grey("Listening...")
            try:
                audio = recognizer.listen(source, timeout=speech_timeout, phrase_time_limit=phrase_time_limit)
                user_input = recognizer.recognize_google(audio, language=language)
                print_green(f"You: {user_input}")

                messages.append({"role": "user", "content": user_input})
                messages = messages[-message_history_limit:]

                print_grey("Processing request...")
                response = openai.ChatCompletion.create(
                    model=openai_model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature
                )

                assistant_reply = response['choices'][0]['message']['content']
                print_blue(f"Assistant: {assistant_reply}")

                if use_pyttsx3:
                    tts_engine.say(assistant_reply)
                    tts_engine.runAndWait()
                elif use_elevenlabs:
                    elevenlabs_speak(assistant_reply)

                messages.append({"role": "assistant", "content": assistant_reply})

            except sr.UnknownValueError:
                print_red("Error: I didn't understand. Please try again.")
            except sr.RequestError as e:
                print_red(f"Error: Server issue: {e}")
            except Exception as e:
                print_red(f"Error: {e}")
finally:
    print_grey("Terminating sprite process...")
    sprite_process.terminate()
    sprite_process.wait()
    print_grey("Sprite process terminated.")