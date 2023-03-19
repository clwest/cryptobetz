from django.core.management.base import BaseCommand
from coingecko.models import Derivative

import requests
from dotenv import load_dotenv
import os
load_dotenv()

coingecko = os.getenv('COINGECKO')


class Command(BaseCommand):
    help = 'Imports Derivative data from an external API'

    def handle(self, *args, **options):
        url = 'https://pro-api.coingecko.com/api/v3/derivatives/exchanges'
        headers = {
            'Accepts': 'application/json',
            'X-CG-Pro-API-Key': coingecko
        }
        params = {'per_page': 200, 'page': 1}
        derivatives = []

        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        # print(data)
        derivatives.extend(data)

        while len(data) == 200:
            params['page'] += 1
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            derivatives.extend(data)

        print(f"Found {len(derivatives)} Derivative")
        
        for derivative in derivatives:
            try:
                if 'status' in derivative:
                    print(f"Failed to import Derivative: {derivative['status']['error_message']}")
                    continue

                url = f'https://pro-api.coingecko.com/api/v3/derivatives/exchanges/{derivative["id"]}'
                response = requests.get(url, headers=headers)

                # print(f"API response: {response.json()}")

                derivative_data = response.json()

                if 'name' not in derivative_data:
                    print(f"Failed to import Derivative: {derivative_data}")
                    continue

                derivative_obj = Derivative.objects.create(
                    name=derivative_data['name'],
                    description=derivative_data['description'],
                    volume_24h=derivative_data['trade_volume_24h_btc'],
                    open_interest_btc=derivative_data['open_interest_btc'],
                    number_of_perpetual_pairs=derivative_data['number_of_perpetual_pairs'],
                    number_of_futures_pairs=derivative_data['number_of_futures_pairs'],
                    year_established=derivative_data['year_established'],
                    country=derivative_data['country'],
                    image=derivative_data['image'],
                    url=derivative_data['url']
                )
            except Exception as e:
                print(f"Failed to import Derivative: {derivative}\nError: {e}")
