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
AUDIO_FORMAT = 'mp3'

# Telegram client
client = TelegramClient('tiktok_tts_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

user_text = {}

voices_list = [
    "1. English US - Female",
    "2. English US - Male 1",
    "3. English US - Male 2",
    "4. English US - Male 3",
    "5. English US - Male 4",
    "6. English UK - Male 1",
    "7. English UK - Male 2",
    "8. English AU - Female",
    "9. English AU - Male",
    "10. French - Male 1",
    "11. French - Male 2",
    "12. German - Female",
    "13. German - Male",
    "14. Spanish - Male",
    "15. Spanish MX - Male 1",
    "16. Spanish MX - Male 2",
    "17. Spanish MX - Female 1",
    "18. Spanish MX - Female 2",
    "19. Spanish MX - Female 3",
    "20. Spanish MX - Optimus Prime (Transformers)",
    "21. Portuguese BR - Female 2",
    "22. Portuguese BR - Female 3",
    "23. Portuguese BR - Male",
    "24. Indonesian - Female",
    "25. Japanese - Female 1",
    "26. Japanese - Female 2",
    "27. Japanese - Female 3",
    "28. Japanese - Male",
    "29. Korean - Male 1",
    "30. Korean - Male 2",
    "31. Korean - Female",
    "32. Characters - Ghostface (Scream)",
    "33. Characters - Chewbacca (Star Wars)",
    "34. Characters - C3PO (Star Wars)",
    "35. Characters - Stitch (Lilo & Stitch)",
    "36. Characters - Stormtrooper (Star Wars)",
    "37. Characters - Rocket (Guardians of the Galaxy)",
    "38. Singing - Alto",
    "39. Singing - Tenor",
    "40. Singing - Sunshine Soon",
    "41. Singing - Warmy Breeze",
    "42. Singing - Glorious",
    "43. Singing - It Goes Up",
    "44. Singing - Chipmunk",
    "45. Singing - Dramatic"
]

voices_map = {
    "1": "en_us_001",
    "2": "en_us_006",
    "3": "en_us_007",
    "4": "en_us_009",
    "5": "en_us_010",
    "6": "en_uk_001",
    "7": "en_uk_003",
    "8": "en_au_001",
    "9": "en_au_002",
    "10": "fr_001",
    "11": "fr_002",
    "12": "de_001",
    "13": "de_002",
    "14": "es_002",
    "15": "es_mx_002",
    "16": "es_male_m3",
    "17": "es_female_f6",
    "18": "es_female_fp1",
    "19": "es_mx_female_supermom",
    "20": "es_mx_male_transformer",
    "21": "br_003",
    "22": "br_004",
    "23": "br_005",
    "24": "id_001",
    "25": "jp_001",
    "26": "jp_003",
    "27": "jp_005",
    "28": "jp_006",
    "29": "kr_002",
    "30": "kr_004",
    "31": "kr_003",
    "32": "en_us_ghostface",
    "33": "en_us_chewbacca",
    "34": "en_us_c3po",
    "35": "en_us_stitch",
    "36": "en_us_stormtrooper",
    "37": "en_us_rocket",
    "38": "en_female_f08_salut_damour",
    "39": "en_male_m03_lobby",
    "40": "en_male_m03_sunshine_soon",
    "41": "en_female_f08_warmy_breeze",
    "42": "en_female_ht_f08_glorious",
    "43": "en_male_sing_funny_it_goes_up",
    "44": "en_male_m2_xhxs_m03_silly",
    "45": "en_female_ht_f08_wonderful_world"
}

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
    voice_buttons = [Button.inline(f"{i}. {voice}", data=voices_map[str(i)].encode()) for i, voice in enumerate(voices_list, start=1)]
    voice_buttons_rows = [voice_buttons[i:i+3] for i in range(0, len(voice_buttons), 3)]  
    await event.reply(f"Now, select a voice:", buttons=[voice_buttons_rows])

    
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
            audio_file = io.BytesIO(audio_data)
            audio_file.name = f"audio.{AUDIO_FORMAT}"
            await client.send_file(event.chat_id, audio_file)
        else:
            await event.reply("Failed to generate audio.")
    else:
        await event.reply("No text entered. Please enter text first.")

def main():
    if not check_service_availability():
        return
    print("Bot is running...")
    try:
        client.run_until_disconnected()
    except Exception as e:
        print(f"Error running bot: {e}")

if __name__ == "__main__":
    main()
