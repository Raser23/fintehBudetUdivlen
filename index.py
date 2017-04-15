import telebot
import config

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands = ['start'])
def repeat_all_messages(message):
    bot.send_message(message.chat.id,config.start_message)

if __name__ == '__main__':
    bot.polling(none_stop=True)
