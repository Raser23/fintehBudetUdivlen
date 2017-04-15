import telebot
import config
import re
import random
import models
import time
import robo_bitch

from utils import delay

@delay(0.01)
def my_func(arg1, arg2):
    notify_all_users()
    my_func(arg1,arg2)

if __name__ == '__main__':
    my_func('Hello', 'world')


print('bot started')

waiting_answer_from_user = {}

secure_random = random.SystemRandom()
remove_whitespace = re.compile('/^\s*([\S\s]*?)\s*$/')
bot = telebot.TeleBot(config.token)

@bot.message_handler(commands = ['start'])
def repeat_all_messages(message):
    bot.send_message(message.chat.id,config.start_message)

@bot.message_handler(content_types=["text"] )
def text_handler(message):
    id = message.chat.id
    message_text = norm_text(message.text).lower()

    if id in waiting_answer_from_user.keys() and waiting_answer_from_user[id].waiting_response:
        if(message_text == 'да'):
            send_message(id, config.point_prediction)
        elif (message_text == 'нет'):
            send_message(id,config.unpoint_prediction)
        else:
            pass
        waiting_answer_from_user[id].waiting_response = False
    else:
        if message_text in config.unimportant_messages:
            reaction_on_unimp_messages(message)
        else:
            prediction(message, message_text)


@bot.message_handler(content_types=["sticker"] )
def handle_sticker(message):
    pass
def prediction(message,text):
    #bot.send_message(message.chat.id, config.get_message)
    ind,theme_name = robo_bitch.predict(text.lower())
    bot.send_message(message.chat.id, config.prediction_message % theme_name)
    start_waiting_answer_from_user(message.chat.id)

def start_waiting_answer_from_user(id):
    waiting_answer_from_user[id] = models.waitAns(id , True)


def reaction_on_unimp_messages(message):
    r = secure_random.random()
    if(r >= 0.5):
        bot.send_sticker(message.chat.id, secure_random.choice(config.stickers_id))
    else:
        bot.send_message(message.chat.id,secure_random.choice(config.emotes))
def norm_text(text):
    r = re.compile(' /  +/g')
    start_ind = 0
    for i in range(len(text)):
        if text[i] == ' ':
            start_ind +=1
        else:
            break
    revt = text[::-1]
    end_ind = len(text)
    for i in range(len(text)):
        if revt[i] == ' ':
            start_ind -= 1
        else:
            break
    res = text[start_ind:end_ind]
    while '  ' in res:
        res = res.replace('  ',' ')
    return res

def send_message(id,text):
    bot.send_message(id,text)

def notify_all_users():
    current_time = time.time()
    for user_ind in waiting_answer_from_user:
        user = waiting_answer_from_user[user_ind]
        if(user.waiting_response):
            if( current_time >= user.start_wait_time + config.first_notify_time) and not user.first_notify:
                send_message(user.user_id,config.first_notify)
                waiting_answer_from_user[user.user_id].first_notify = True
            if( current_time >= user.start_wait_time + config.stop_notife_time) and user.first_notify :
                waiting_answer_from_user[user.user_id].waiting_response = False;

if __name__ == '__main__':
    bot.polling(none_stop=True)







