from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from python_telegram_bot import telegram
import logging
from gtts import gTTS 
from tempfile import TemporaryFile 
import secrets
import os
import botan
from datetime import datetime

bot = telegram.Bot(token=secrets.bot_token)
# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

def generate_tts(text, lang):
    tts = gTTS(text=text, lang=lang)  

    filename = datetime.now()
    if not os.path.exists('audios'):
        os.makedirs('audios')
    
    tts.save('audios/%s.ogg'%filename)

    return filename

def start(bot, update):
    bot.sendVoice(chat_id=update.message.chat_id, voice=open('hello.ogg', 'rb'))
    bot.sendMessage(update.message.chat_id, text="Hi! I'm TTSpeechBot. To use: /tts [lang] [menssage], for example: /tts en I'm TTSBot!", parse_mode=telegram.ParseMode.HTML)

def help(bot, update):
    bot.sendMessage(update.message.chat_id, text="To use: /tts [lang] [menssage], for example: /tts en I'm TTSBot!", parse_mode=telegram.ParseMode.HTML)

def tts(bot, update):
    botan_token = 'xlNvNez4gmhcxHLrZpLc4fNUPzjCx2U9'
    uid = update.message.from_user.id
    message_dict = update.message.to_dict()
    event_name = update.message.text[4:]
    print (botan.track(botan_token, uid, message_dict, event_name))

    try:
        filename = generate_tts(update.message.text[8:], update.message.text[5:7])
    except:
        filename = False
        bot.sendMessage(update.message.chat_id, text="There has been an issue with Google, please try again later.")
    
    if filename != False:
        try:
            bot.sendVoice(chat_id=update.message.chat_id, voice=open('audios/%s.ogg'%filename, 'rb'))
        except:
            echo(bot,update)

def otts(bot,update):
    botan_token = 'xlNvNez4gmhcxHLrZpLc4fNUPzjCx2U9'
    uid = update.message.from_user.id
    message_dict = update.message.to_dict()
    event_name = update.message.text[5:]
    print (botan.track(botan_token, uid, message_dict, event_name))
    try:
        filename = generate_tts('Fucking' + update.message.text[9:], update.message.text[6:8])
        bot.sendVoice(chat_id=update.message.chat_id, voice=open('audios/%s.ogg'%filename, 'rb'))
    except:
        bot.sendMessage(update.message.chat_id, text="Please, use the right format: /otts [lang] [menssage], for example: /tts en I'm TTSBot!")

def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text="Please, use the right format: /tts [lang] [menssage], for example: /tts en I'm TTSBot!")

def developer(bot, update):
    bot.sendMessage(update.message.chat_id, text='Made by @Rogergonzalez21 with a lot of help from @sergsss. GitHub repo: https://github.com/Rogergonzalez21/telegram_tts_bot')

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(secrets.bot_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addHandler(CommandHandler("start", start))
    dp.addHandler(CommandHandler("help", help))
    dp.addHandler(CommandHandler("tts", tts))
    dp.addHandler(CommandHandler("otts", otts))
    dp.addHandler(CommandHandler("developer", developer))


    # on noncommand i.e message - echo the message on Telegram
    dp.addHandler(MessageHandler([Filters.text], echo))

    # log all errors
    dp.addErrorHandler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()