import openai
import logging
import os

import telebot


OPENAI_API_KEY = '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'
openai.api_key = OPENAI_API_KEY

TELEGRAM_API_KEY = '6062770696:AAErZvC0BpyV3O7abMH6gQGIIntucph896I'
bot = telebot.TeleBot(TELEGRAM_API_KEY)

start_chat_log = [
    {
        "role": "system",
        "content": " Hallo, MILF , do you want my d...k?"
    }
]

chat_log = None
completion = openai.ChatCompletion()



def ask(question, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    prompt2 = [{"role": "user", "content": f"{question}"}]
    prompt = chat_log + prompt2

    response = completion.create(  # type: ignore
        messages=prompt,
        model="gpt-3.5-turbo",
    )
    answer = [response.choices[0].message]  # type: ignore
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

        logging.info(f"\n\nUser {text}\n**********AI: {response}")

        return response[0].content

    except Exception as e:
        chat_log = start_chat_log
        return f"Wait a minute please....{e}"


def get_chat_bot_response(question, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    prompt2 = [{"role": "user", "content": f"{question}"}]
    prompt = chat_log + prompt2

    response = completion.create(
        messages=prompt,
        model="gpt-3.5-turbo"
    )
    answer = [response.choices[0].message]  # type: ignore
    return answer

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    response = handle_message(message.text)
    bot.reply_to(message, response)

bot.polling()