import telebot
import config
import re
import random

secure_random = random.SystemRandom()
remove_whitespace = re.compile('/^\s*([\S\s]*?)\s*$/')

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands = ['start'])
def repeat_all_messages(message):
    bot.send_message(message.chat.id,config.start_message)

@bot.message_handler(content_types=["text"] )
def text_handler(message):
    message_text = norm_text(message.text)

    if message_text in config.unimportant_messages:
        reaction_on_unimp_messages(message)
    else:
        bot.send_message(message.chat.id, config.get_message)
        bot.send_message(message.chat.id,config.prediction_message % prediction(message_text))

@bot.message_handler(content_types=["sticker"] )
def handle_sticker(message):
    pass

def prediction(text):
    return "банкоматы"

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



if __name__ == '__main__':
    bot.polling(none_stop=True)
