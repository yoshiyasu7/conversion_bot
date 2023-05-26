"""Каркас телеграм бота"""
import telebot
from config import currencies, TOKEN
from extensions import UserException, ApiRequest

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def helping(message: telebot.types.Message):
    text = 'Чтобы узнать стоимость валюты, введите параметры боту в следующем ' \
           'формате:\n"Название валюты" "В какую валюту перевести" "Колличество"' \
           '\nУвидеть список доступных валют: /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def convert(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for k in currencies.keys():
        text = '\n'.join((text, k, ))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise UserException('Неправильный ввод параметров.')

        quote, base, amount = values
        price = ApiRequest.get_price(quote.lower(), base.lower(), amount)

    except UserException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')

    else:
        text = f'Курс {amount} {quote} в {base}: {price}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
