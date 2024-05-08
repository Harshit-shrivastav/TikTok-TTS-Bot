import io, os
from telethon import TelegramClient, events, Button
from functions import *

API_ID = int(os.environ.get("API_ID"))
API_HASH = str(os.environ.get("API_HASH"))
BOT_TOKEN = str(os.environ.get("BOT_TOKEN"))

TEXT_BYTE_LIMIT = 300
AUDIO_FORMAT = 'mp3'

client = TelegramClient('tiktok_tts_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

user_text = {}

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    await event.reply('Hello! Send me some text, and I will convert it to speech using the TikTok TTS service.', buttons=[Button.url("Source Code", url="https://github.com/Harshit-shrivastav/TikTok-TTS-Bot")])

@client.on(events.NewMessage(func=lambda e: e.is_private and not e.text.startswith('/'), pattern=r'(?!^/).*'))
async def text_input_handler(event):
    user_id = event.sender_id
    user_text[user_id] = event.text
    voice_buttons = []
    for i in range(0, len(voices_list), 2):
        chunk = voices_list[i:i + 2]
        row = [Button.inline(voice_label, data=voices_map[str(index)].encode()) for index, voice_label in enumerate(chunk, start=i + 1)]
        voice_buttons.append(row)
    await event.reply(f'Your Input: "{event.text}"\nNow, select a voice:', buttons=voice_buttons)

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

    print("Bot is running...\nHit ⭐ to github repo, if you liked my work.\nWritten by Harshit-shrivastav.")
    try:
        client.run_until_disconnected()
    except Exception as e:
        print(f"Error running Telegram bot: {e}")

if __name__ == "__main__":
    main()
