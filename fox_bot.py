import openai
from dotenv import load_dotenv
from telebot import types
import logging
import os

import telebot

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
bot = telebot.TeleBot(TELEGRAM_API_KEY)

start_chat_log = [
    {
        "role": "system",
        "content": "Вы общаетесь с ,ботом-Алисы, дружелюбной и веселой девушкой. Она всегда готова помочь вам с вопросами или просто поболтать!"
    }
]

chat_log = None
completion = openai.ChatCompletion()

def ask(question, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    prompt2 = [{"role": "user", "content": f"{question}"}]
    prompt = chat_log + prompt2

    response = completion.create(
        messages=prompt,
        model="gpt-3.5-turbo",
    )
    answer = [response.choices[0].message]
    return answer

def append_interaction_to_chat_log(question, answer, chat_log):
    if chat_log is None:
        chat_log = start_chat_log
    prompt2 = [{"role": "user", "content": f"{question}"}]
    return chat_log + prompt2 + answer

def handle_message(text):
    try:
        global chat_log
        question = f"{text}"
        response = ask(question, chat_log)
        chat_log = append_interaction_to_chat_log(question, response, chat_log)

        return response[0].content

    except Exception as e:
        chat_log = start_chat_log
        return f"Пожалуйста, подождите минутку...{e}"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Алиса сейчас занята, но я здесь, чтобы общаться. Давай поговорим! Как тебя зовут?")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    response = handle_message(message.text)
    bot.reply_to(message, response)

bot.polling()
