import telebot
import config
import re
import random
import models
import time
import robo_bitch
import point_callbacks
from telebot import types
from utils import delay
import utils
stored_messages = {}
unright_detect = {}
@delay(0.01)
def notify_users_updater():
    notify_all_users()
    notify_users_updater()


print('Bot started')

waiting_answer_from_user = {}
notifications = {}

secure_random = random.SystemRandom()
remove_whitespace = re.compile('/^\s*([\S\s]*?)\s*$/')
bot = telebot.TeleBot(config.token)

def message_sender(id,markup):
    def the_wrapper(text):
        if(markup):
            send_message(id,text,reply_markup = markup)
        else:
            send_message(id, text)
    return the_wrapper
@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message(message.chat.id,config.start_message)

@bot.message_handler(content_types=["text"] )
def text_handler(message):

    id = message.chat.id
    if id in notifications:
        del notifications[id]
    message_text = norm_text(message.text).lower()

    if id in waiting_answer_from_user.keys() and waiting_answer_from_user[id].waiting_response:
        markup = types.ReplyKeyboardRemove()
        if message_text in config.positive_answers:
            unright_detect[id] = 0
            send_message(id, config.point_prediction)
            theme_id = waiting_answer_from_user[id].sended_theme
            if theme_id in point_callbacks.callbacks.keys():
                point_callbacks.callbacks[theme_id](message_sender(id,markup))
        elif (message_text in config.negative_answers):
            send_message(id,config.unpoint_prediction,reply_markup=markup)
            unright_detect.setdefault(id, 0)
            unright_detect[id] += 1
            if(unright_detect[id] >= 3):
                send_message(id, config.streak3)
                unright_detect[id] = 0
            else:
                notifications[id] = models.motification(id,config.help_message,config.notification_delay)
                pass
        else:
            pass
        waiting_answer_from_user[id].waiting_response = False
    else:
        if message_text in config.unimportant_messages or message_text in config.emotes:
            reaction_on_unimp_messages(message)
        else:
            stored_messages.setdefault(id, [])
            stored_messages[id].append(message_text)
            prediction(message, message_text)


@bot.message_handler(content_types=["sticker"] )
def handle_sticker(message):
    print(message.sticker)
    pass
def prediction(message,text):
    user_id = message.chat.id
    error_streak = 0
    if user_id in unright_detect:
        error_streak = unright_detect[user_id]


    analyze_text = text
    if (error_streak > 0):
        #print(stored_messages[user_id])
        analyze_text += ' '+stored_messages[user_id][-2]
    #print(analyze_text)
    ind,theme_name = robo_bitch.predict(analyze_text.lower())
    markup = utils.generate_markup('да','нет')
    bot.send_message(message.chat.id, config.prediction_message % theme_name,reply_markup=markup)
    start_waiting_answer_from_user(message.chat.id,ind)

def start_waiting_answer_from_user(id,theme_id):
    waiting_answer_from_user[id] = models.waitAns(id , True,theme_id)

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

def send_message(id,text,reply_markup = None):
    bot.send_message(id,text,reply_markup=reply_markup)

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
    delete = []
    for user_ind in notifications:
        user = notifications[user_ind]
        if current_time >= user.start_wait_time + config.notification_delay and not user.first_notify:
            send_message(user.user_id, config.help_message)
            notifications[user_ind].first_notify = True
        if current_time >= user.start_wait_time + config.notification_delay2 and user.first_notify:
            send_message(user.user_id, config.restart_message)
            unright_detect[user_ind] = 0
            delete.append(user_ind)

    for i in delete:
        del notifications[i]

if __name__ == '__main__':
    notify_users_updater()
    bot.polling(none_stop=True)









