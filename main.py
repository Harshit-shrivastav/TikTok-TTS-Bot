import os
import requests
import json
import base64
from telethon import TelegramClient, sync, events, Button

# Telegram bot configuration
API_ID = 4680197
API_HASH = '495b0228624028d635bd748b22985f67'
BOT_TOKEN = '5810975688:AAHc57W24SQu6_Nb9KnsW0eOxEgbsRmVImo'

# TikTok TTS configuration
ENDPOINT = 'https://tiktok-tts.weilnet.workers.dev'
TEXT_BYTE_LIMIT = 300

# Telegram client
client = TelegramClient('tiktok_tts_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

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
    except Exception as e:
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
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    await event.respond('Hello! Send me some text, and I will convert it to speech using the TikTok TTS service.')

@client.on(events.NewMessage(pattern='/voices'))
async def voices_handler(event):
    voice_buttons = [
        [Button.inline("English US - Female", data=b"en_us_001")],
        [Button.inline("English US - Male 1", data=b"en_us_006")],
        # ... (add the rest of the voice options here)
    ]
    await event.respond("Select a voice:", buttons=voice_buttons)

@client.on(events.CallbackQuery())
async def voice_handler(event):
    selected_voice = event.data.decode()
    await event.answer(f"You selected: {selected_voice}")

    # Get the message that triggered the voice selection
    message = await event.get_message()
    text = message.message

    if len(text.encode('utf-8')) > TEXT_BYTE_LIMIT:
        await event.respond(f"Text must not be over {TEXT_BYTE_LIMIT} UTF-8 characters.")
        return

    audio_data = generate_audio(text, selected_voice)
    if audio_data:
        await event.respond(file=audio_data, force_document=True)
    else:
        await event.respond("Failed to generate audio.")

def main():
    if not check_service_availability():
        return

    print("Telegram bot is running...")
    client.run_until_disconnected()

if __name__ == "__main__":
    main()
