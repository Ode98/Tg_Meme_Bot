from logging import exception
import os
import telebot
from niilo_voice import lines
from dotenv import load_dotenv

load_dotenv()

global NIILO_VOICE_PATH
NIILO_VOICE_PATH = os.getenv('NIILO_VOICE_PATH')

token = os.getenv('API_KEY')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, "/niilo näyttää kaikki mahdolliset clipit\n/ääniclipin_nimi antaa ääniclipin :3")


@bot.message_handler(commands=['gibe'])
def OldMemeGen(message):
    bot.send_message(message.chat.id, "/gibe - ei anna enään meemua :/ uusi versio on pelkkä äänibotti :3")    


@bot.message_handler(commands=['niilo', 'niilo22', 'Niilo', 'Niilo22'])
def handle_niilo_help(message):
    bot.send_message(message.chat.id, (', '.join(lines)))


@bot.message_handler(commands=list(lines.keys()))
def handle_niilo_review(message):
    sound = open(f'./niilo22/{lines[message.text[1:]]}' , 'rb')
    bot.send_audio(message.chat.id, sound, '', '', f'{message.from_user.first_name}', f'{lines[message.text[1:]]}')
    handle_delete(message)


@bot.message_handler(func=lambda message : message.text[0] == '/')
def handle_delete(message):
    bot.delete_message(message.chat.id, message.id)


bot.infinity_polling()
