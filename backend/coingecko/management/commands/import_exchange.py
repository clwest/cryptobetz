from django.core.management.base import BaseCommand
from coingecko.models import Exchange
import requests
from dotenv import load_dotenv
import os
load_dotenv()

coingecko = os.getenv('COINGECKO')


class Command(BaseCommand):
    help = 'Imports NFT data from an external API'

    def handle(self, *args, **options):
        url = 'https://pro-api.coingecko.com/api/v3/exchanges'
        headers = {
            'Accepts': 'application/json',
            'X-CG-Pro-API-Key': coingecko
        }
        params = {'per_page': 200, 'page': 1}
        exchanges = []

        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        print(data)
        exchanges.extend(data)

        while len(data) == 200:
            params['page'] += 1
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            exchanges.extend(data)

        print(f"Found {len(exchanges)} Exchanges")
        
        for exchange in exchanges:
            try:
                if 'status' in exchange:
                    print(f"Failed to import Exchange: {exchange['status']['error_message']}")
                    continue

                url = f'https://pro-api.coingecko.com/api/v3/exchanges/{exchange["id"]}'
                response = requests.get(url, headers=headers)

                # print(f"API response: {response.json()}")

                exchange_data = response.json()

                if 'name' not in exchange_data:
                    print(f"Failed to import Exchange: {exchange_data}")
                    continue

                exchange_obj = Exchange.objects.create(
                    name=exchange_data['name'],
                    country = exchange_data['country'],
                    description = exchange_data['description'],
                    url = exchange_data['url'],
                    twitter_handle = exchange_data['twitter_handle'],
                    facebook_url = exchange_data['facebook_url'],
                    telegram_url = exchange_data['telegram_url'],
                    reddit_url = exchange_data['reddit_url'],
                    slack_url = exchange_data['slack_url'],
                    other_url1 = exchange_data['other_url_1'],
                    other_url2 = exchange_data['other_url_2'],
                    centralized = exchange_data['centralized'],
                    trust_score = exchange_data['trust_score'],
                    trust_score_rank = exchange_data['trust_score_rank'],
                    trade_volume_24h_btc = exchange_data['trade_volume_24h_btc'],
                    trade_volume_24h_btc_normalized = exchange_data['trade_volume_24h_btc_normalized'],
                )
            except Exception as e:
                print(f"Failed to import Exchange: {exchange}\nError: {e}")
