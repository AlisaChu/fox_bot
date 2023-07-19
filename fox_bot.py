import telebot
import os

# Substitute 'YOUR_BOT_TOKEN' with your bot's token
bot_token = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Оставьте ваш отзыв")

@bot.message_handler(func=lambda message: True)
def handle_all_message(message):
    try:
        with open('feedback.txt', 'a', encoding='utf-8') as f:
            f.write(f"{message.text}\n")
        bot.reply_to(message, "Ваш отзыв был сохранен. Спасибо!")
    except Exception as e:
        bot.reply_to(message, "Извините, произошла ошибка при сохранении вашего отзыва.")
        print(f"Error: {str(e)}")

bot.polling()