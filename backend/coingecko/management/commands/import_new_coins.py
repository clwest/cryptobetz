from django.core.management.base import BaseCommand
from coingecko.models import NewCoin
import requests
from dotenv import load_dotenv
import os

load_dotenv()

coingecko = os.getenv('COINGECKO')


class Command(BaseCommand):
    help = 'Imports new coin data from Coingecko API'

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

        while data:
            params['page'] += 1
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            new_coins.extend(data)

        print(f"Found {len(new_coins)} New Coins")

        for coin in new_coins:
            try:
                if NewCoin.objects.filter(name=coin['name']).exists():
                    print(f"Coin already exists: {coin['name']}")
                    continue

                new_coin_obj = NewCoin.objects.get_or_create(
                    name=coin['name'],
                    defaults={
                        'symbol': coin['symbol'],
                        'coingecko_id': coin['id'],
                    }
                )
            except Exception as e:
                print(f"Failed to import New Coin: {coin}\nError: {e}")
