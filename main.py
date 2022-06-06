from logging import exception
import os
import telebot
from niilo_voice import lines
from dotenv import load_dotenv

load_dotenv()

global MEME_PATH
global MEME_START_INDEX
global MEME_DATA_PATH
global NIILO_VOICE_PATH

MEME_START_INDEX = 10000 # TODO:

MEME_PATH = os.getenv('MEME_PATH')
NIILO_VOICE_PATH = os.getenv('NIILO_VOICE_PATH')
MEME_DATA_PATH = os.getenv('MEME_DATA_PATH')

token = os.getenv('API_KEY')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, "/gibe - antaa meemun :3")
    handle_delete(message)


@bot.message_handler(commands=['gibe'])
def Greet(message):
    send_img(message)
    handle_delete(message)


@bot.message_handler(commands=['niilo', 'niilo22', 'Niilo', 'Niilo22'])
def handle_niilo_help(message):
    bot.send_message(message.chat.id, (', '.join(lines)))
    handle_delete(message)


@bot.message_handler(commands=list(lines.keys()))
def handle_niilo_review(message):
    voice = open(f'{NIILO_VOICE_PATH}{lines[message.text[1:]]}' , 'rb')
    bot.send_voice(message.chat.id, voice)
    handle_delete(message)


@bot.message_handler(func=lambda message : message.text[0] == '/')
def handle_delete(message):
    bot.delete_message(message.chat.id, message.id)


def send_msg(message_info, message):
    bot.send_message(message_info.chat.id, message)


def send_img(message):
    img = open(next_meme(message), 'rb')
    bot.send_photo(message.chat.id, img)


def next_meme(message):
    with open(MEME_DATA_PATH, "r+") as f:
        img_id = int(f.read())
        f.seek(0)
        f.write(str(img_id +1))
        f.truncate()

    location = (f"{MEME_PATH}\{img_id}")

    if (check_type(location) != None):
        return(check_type(location))
    else:
        if check_for_memes(img_id):
            return send_img(message)
        else:
            send_msg(message, "Meemut loppu :(")


def check_for_memes(img_id):
    for i in range (15):
        if (check_type(f"{MEME_PATH}\{img_id + i}") != None):
            return img_id + 1
    return False


def check_type(location):
    if os.path.exists(location + '.jpg'):
        return(location + '.jpg')
    elif os.path.exists(location + '.png'):
        return(location + '.png')
    else:
        return(None)


def niilo22_ohje():
    return(list(lines.keys()))


bot.infinity_polling()