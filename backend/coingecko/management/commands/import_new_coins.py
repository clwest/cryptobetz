from django.core.management.base import BaseCommand
from coingecko.models import NewCoin
import requests
from dotenv import load_dotenv
import os

load_dotenv()

coingecko = os.getenv('COINGECKO')


class Command(BaseCommand):
    help = 'Imports new coin data from an external API'

    def handle(self, *args, **options):
        url = 'https://pro-api.coingecko.com/api/v3/coins/list/new'
        headers = {
            'Accepts': 'application/json',
            'X-CG-Pro-API-Key': coingecko
        }
        params = {'per_page': 250, 'page': 1}
        new_coins = []

        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        new_coins.extend(data)

        while len(data) == params['per_page']:
            params['page'] += 1
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            new_coins.extend(data)

        print(f"Found {len(new_coins)} New Coins")

        for new_coin_data in new_coins:
            try:
                if 'status' in new_coin_data:
                    print(f"Failed to import New Coin: {new_coin_data['status']['error_message']}")
                    continue

                new_coin_obj = NewCoin.objects.create(
                    name=new_coin_data['name'],
                    symbol=new_coin_data['symbol'],
                    coingecko_id=new_coin_data['id'],
                )
            except Exception as e:
                print(f"Failed to import New Coin: {new_coin_data}\nError: {e}")
