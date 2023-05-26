"""Все классы"""
import requests
import json
from config import currencies, APIKEY


class UserException(Exception):
    pass


class ApiRequest:

    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise UserException(f'Невозможно конвертировать одну валюту {quote}.')

        try:
            keys_q = currencies[quote]
        except KeyError:
            raise UserException(f'Не удалось обработать валюту {quote}.')

        try:
            keys_b = currencies[base]
        except KeyError:
            raise UserException(f'Не удалось обработать валюту {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise UserException(f'Введено неправильное число валюты {amount}.')

        url = f'https://v6.exchangerate-api.com/v6/{APIKEY}/pair/{keys_q}/{keys_b}/{amount}'
        r = requests.get(url)
        price = json.loads(r.content)['conversion_result']

        return price
