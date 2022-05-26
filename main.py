from logging import exception
import os
import telebot
from niilo_voice import lines
from dotenv import load_dotenv

load_dotenv()

global meme_path
global meme_start_index
global meme_data_path
global niilo_voice_path

meme_start_index = 10000

meme_path = os.getenv('MEME_PATH') #path to meme folder (only jpg and png supported)
niilo_voice_path = os.getenv('NIILO_VOICE_PATH') #(#path to voicelines folder)
meme_data_path = os.getenv('MEME_DATA_PATH') #path to data of meme indexes / filenames

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
    voice = open(f'{niilo_voice_path}{lines[message.text[1:]]}' , 'rb')
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
    with open(meme_data_path, 'r') as f:
        img_id = int(f.read())
    with open(meme_data_path, 'w') as f:
        f.write(str(img_id +1))

    location = (f"{meme_path}\{img_id}")

    if (check_type(location) != None):
        return(check_type(location))
    else:
        if check_for_memes(img_id):
            send_img(message)
        else:
            send_msg(message, "@Ode lisää meemuja kantaan laiska paska :3")
            with open(meme_data_path, 'w') as f:
                f.write(str(meme_start_index))


def check_for_memes(img_id):
    for i in range (15):
        if (check_type(f"{meme_path}\{img_id + i}") != None):
            return True
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
