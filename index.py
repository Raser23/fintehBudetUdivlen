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
keyboard_choose_notifications = {}

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

    if id in keyboard_choose_notifications:
        del keyboard_choose_notifications[id]
    if id in waiting_answer_from_user.keys() and waiting_answer_from_user[id].waiting_response:
        if type(waiting_answer_from_user[id].sended_theme) is int:
            solo_answer(message_text,id)
        else:
            multy_answer(message_text,id)

    else:
        #print(message_text)
        if message_text in config.unimportant_messages or message_text in config.emotes:
            reaction_on_unimp_messages(message)
        else:
            stored_messages.setdefault(id, [])
            stored_messages[id].append(message_text)
            prediction(message, message_text)


def solo_answer(message_text,user_id):
    markup = types.ReplyKeyboardRemove()
    #print(message_text)
    if message_text in config.positive_answers:
        unright_detect[user_id] = 0
        send_message(user_id, config.point_prediction)
        theme_id = waiting_answer_from_user[user_id].sended_theme
        if theme_id in point_callbacks.callbacks.keys():
            point_callbacks.callbacks[theme_id](message_sender(user_id, markup))
    elif (message_text in config.negative_answers):

        unright_detect.setdefault(user_id, 0)
        unright_detect[user_id] += 1
        if (unright_detect[user_id] >= 3):
            send_message(user_id, config.streak3)
            unright_detect[user_id] = 0
        else:
            send_message(user_id, config.unpoint_prediction, reply_markup=markup)
            notifications[user_id] = models.motification(user_id, config.help_message, config.notification_delay)
            pass
    waiting_answer_from_user[user_id].waiting_response = False
unright_choosed_streak = {}
def form_list(predictions,start_text = config.multy_predict_message):
    text = start_text
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for p in predictions:
        text += '\n' + str(p[0]) + '-' + str(p[1])
        markup.add(str(p[0]))
    markup.add(config.no_one)
    return text,markup
def multy_answer(message_text,user_id):
    variants = waiting_answer_from_user[user_id].sended_theme

    if( message_text.lower() == config.no_one.lower()):
        solo_answer('нет',user_id)
    else:
        choosed = (-1,-1)
        for v in variants:
            if str(v[0]).lower() == str(message_text).lower():
                choosed = v
        if(choosed[0] == -1):
            unright_choosed_streak.setdefault(user_id,0)
            unright_choosed_streak[user_id]+=1
            if(unright_choosed_streak[user_id] < 3):
                text, markup = form_list(waiting_answer_from_user[user_id].sended_theme,start_text=config.more_point_text)
                keyboard_choose_notifications[user_id] = models.motification(user_id,text,config.first_notify_time,markup)
                bot.send_message(user_id,'Номер темы был казан неправильно.\n'+text,markup)
            else:
                bot.send_message(user_id,config.restart_message,reply_markup=types.ReplyKeyboardRemove())
                unright_choosed_streak[user_id] = 0
                waiting_answer_from_user[user_id].waiting_response = False
            pass
        else:
            unright_choosed_streak.setdefault(user_id,0)
            unright_choosed_streak[user_id] = 0
            waiting_answer_from_user[user_id].waiting_response = False
            waiting_answer_from_user[user_id].sended_theme = choosed[0]

            solo_answer('да',user_id)





@bot.message_handler(content_types=["sticker"] )
def handle_sticker(message):
    if message.sticker.emoji in config.emotes:
        reaction_on_unimp_messages(message)
    pass
def prediction(message,text):
    user_id = message.chat.id
    error_streak = 0
    if user_id in unright_detect:
        error_streak = unright_detect[user_id]


    analyze_text = text
    if (error_streak > 0):
        analyze_text = stored_messages[user_id][-2]+' ' + analyze_text
    print(analyze_text)
    predictions = robo_bitch.predict(analyze_text.lower())
    if(len( predictions) == 1):
        markup = utils.generate_markup('да', 'нет')
        bot.send_message(message.chat.id, config.prediction_message % predictions[0][1],reply_markup=markup)
        start_waiting_answer_from_user(message.chat.id, int(predictions[0][0]))
    else:
        text,markup = form_list(predictions,start_text=config.more_point_text)
        bot.send_message(message.chat.id,text,reply_markup=markup)
        start_waiting_answer_from_user(user_id,predictions)
        keyboard_choose_notifications[user_id] = models.motification(user_id, text, config.first_notify_time, markup)
        pass

def start_waiting_answer_from_user(id,theme_id):
    waiting_answer_from_user[id] = models.waitAns(id , True,theme_id)

def reaction_on_unimp_messages(message):
    r = secure_random.random()
    if(r <= 0.33333):
        bot.send_sticker(message.chat.id, secure_random.choice(config.stickers_id))
    elif(r<=0.666666):
        bot.send_message(message.chat.id,secure_random.choice(config.positive_phrases))
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
        #print(user.waiting_response)
        if(user.waiting_response == True):
            if(not type(user.sended_theme)  is int):
                continue
            if( current_time >= user.start_wait_time + config.first_notify_time) and not user.first_notify:
                send_message(user.user_id,config.first_notify)
                print('message sended')
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

    delete = []
    for user_ind in keyboard_choose_notifications:
        user = keyboard_choose_notifications[user_ind]
        #print(user)
        if current_time >= user.start_wait_time + config.notification_delay and not user.first_notify:
            send_message(user.user_id, user.text)
            keyboard_choose_notifications[user_ind].first_notify = True
        if current_time >= user.start_wait_time + config.notification_delay2 and user.first_notify:
            #print('deleted')
            waiting_answer_from_user[user.user_id].waiting_response = False;
            unright_detect[user_ind] = 0
            delete.append(user_ind)

    for i in delete:

        del keyboard_choose_notifications[i]

if __name__ == '__main__':
    notify_users_updater()
    bot.polling(none_stop=True)









