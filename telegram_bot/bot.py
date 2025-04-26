from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

API_BASE_URL = "http://localhost:8000/api/voice-chat"

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Send me your voice, and I'll answer!")

def voice(update: Update, context: CallbackContext):
    file = update.message.voice.get_file()
    file.download("received_voice.ogg")

    with open("received_voice.ogg", "rb") as audio_file:
        response = requests.post(API_BASE_URL, files={"file": audio_file})

    with open("response.mp3", "wb") as audio_file:
        audio_file.write(response.content)

    with open("response.mp3", "rb") as audio_file:
        update.message.reply_voice(voice=audio_file)

def main():
    updater = Updater("YOUR-TELEGRAM-BOT-TOKEN", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.voice, voice))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
