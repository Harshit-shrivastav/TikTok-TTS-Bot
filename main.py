import os
import requests
import json
import base64
import io
from telethon import TelegramClient, sync, events, Button

# Telegram bot configuration
API_ID = 4680197
API_HASH = '495b0228624028d635bd748b22985f67'
BOT_TOKEN = '5810975688:AAHc57W24SQu6_Nb9KnsW0eOxEgbsRmVImo'

# TikTok TTS configuration
ENDPOINT = 'https://tiktok-tts.weilnet.workers.dev'
TEXT_BYTE_LIMIT = 300
AUDIO_FORMAT = 'mp3'  # or 'wav'

# Telegram client
client = TelegramClient('tiktok_tts_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# In-memory storage for text input
user_text = {}

def check_service_availability():
    try:
        response = requests.get(f"{ENDPOINT}/api/status")
        data = response.json()
        if response.status_code == 200 and data.get('data') and data['data'].get('available'):
            print(f"{data['data']['meta']['dc']} (age {data['data']['meta']['age']} minutes) is able to provide service")
            return True
        else:
            print(f"Service is unavailable: {data.get('message', 'Unknown error')}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error querying API status: {e}")
        return False

def generate_audio(text, voice):
    try:
        response = requests.post(f"{ENDPOINT}/api/generation", json={"text": text, "voice": voice})
        if response.status_code == 200:
            data = response.json()
            if data.get('data'):
                # Decode base64-encoded audio data
                audio_data = base64.b64decode(data['data'])
                return audio_data
            else:
                print(f"Generation failed: {data.get('error', 'Unknown error')}")
                return None
        else:
            print(f"Failed to generate audio: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error generating audio: {e}")
        return None

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    await event.reply('Hello! Send me some text, and I will convert it to speech using the TikTok TTS service.')

@client.on(events.NewMessage(func=lambda e: e.is_private and not e.text.startswith('/'), pattern=r'(?!^/).*'))
async def text_input_handler(event):
    user_id = event.sender_id
    user_text[user_id] = event.text

    voice_buttons = [
        [Button.inline("English US - Female", data=b"en_us_001")],
        [Button.inline("English US - Male 1", data=b"en_us_006")],
    ]
    await event.reply(f"You entered: {event.text}\nNow, select a voice:", buttons=voice_buttons)

@client.on(events.CallbackQuery())
async def voice_selection_handler(event):
    user_id = event.sender_id
    selected_voice = event.data.decode()
    await event.answer(f"You selected: {selected_voice}")

    if user_id in user_text:
        text = user_text[user_id]
        if len(text.encode('utf-8')) > TEXT_BYTE_LIMIT:
            await event.reply(f"Text must not be over {TEXT_BYTE_LIMIT} UTF-8 characters.")
            return

        audio_data = generate_audio(text, selected_voice)
        if audio_data:
            # Save audio data to a temporary file
            audio_file = io.BytesIO(audio_data)
            audio_file.name = f"audio.{AUDIO_FORMAT}"

            # Send the audio file
            await client.send_file(event.chat_id, audio_file)
        else:
            await event.reply("Failed to generate audio.")
    else:
        await event.reply("No text entered. Please enter text first.")

def main():
    if not check_service_availability():
        return

    print("Telegram bot is running...")
    try:
        client.run_until_disconnected()
    except Exception as e:
        print(f"Error running Telegram bot: {e}")

if __name__ == "__main__":
    main()
