from asgiref.sync import async_to_sync
import requests

from celery import shared_task
from channels.layers import get_channel_layer
from django.forms.models import model_to_dict

from .models import Coin


channel_layer = get_channel_layer()

@shared_task
def get_coins_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': '20',
        'page': '1',
        'sparkline': 'false'
    }
    data = requests.get(url=url, params=params).json()

    coins = []

    for coin in data:
        obj, created = Coin.objects.get_or_create(symbol=coin['symbol'])

        obj.name = coin['name']
        obj.rank = coin['market_cap_rank']
        obj.image = coin['image']

        if obj.price < coin['current_price']:
            state = 'incr'
        elif obj.price == coin['current_price']:
            state = 'equal'
        elif obj.price > coin['current_price']:
            state = 'decr'
        obj.price = coin['current_price']

        obj.save()

        new_coins_data = model_to_dict(obj)
        new_coins_data.update({'state': state})

        coins.append(new_coins_data)

    async_to_sync(channel_layer.group_send)('coins', {'type': 'send_new_data', 'text': coins})
