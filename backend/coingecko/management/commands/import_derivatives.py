from django.core.management.base import BaseCommand
from coingecko.models import Derivative
import requests
import os
from dotenv import load_dotenv

load_dotenv()
coingecko = os.getenv('COINGECKO')

class Command(BaseCommand):
    help = 'Imports Derivative data from the Coingecko API'

    def handle(self, *args, **options):
        url = 'https://pro-api.coingecko.com/api/v3/derivatives/exchanges'
        headers = {
            'Accepts': 'application/json',
            'X-CG-Pro-API-Key': coingecko
        }
        params = {'per_page': 200, 'page': 1}
        derivatives = []

        while True:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            derivatives.extend(data)

            if len(data) < 200:
                break

            params['page'] += 1

        print(f"Found {len(derivatives)} Derivatives")

        for derivative in derivatives:
            try:
                if Derivative.objects.filter(name=derivative['name']).exists():
                    print(f"Derivative already exists: {derivative['name']}")
                    continue

                url = f'https://pro-api.coingecko.com/api/v3/derivatives/exchanges/{derivative["id"]}'
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                derivative_data = response.json()

                if 'name' not in derivative_data:
                    print(f"Failed to import Derivative: {derivative_data}")
                    continue

                derivative_obj, created = Derivative.objects.get_or_create(
                    name=derivative_data['name'],
                    defaults = {
                        'description': derivative_data.get('description', ''),
                        'volume_24h': derivative_data.get('trade_volume_24h_btc', 0),
                        'open_interest_btc': derivative_data.get('open_interest_btc', 0),
                        'number_of_perpetual_pairs': derivative_data.get('number_of_perpetual_pairs', 0),
                        'number_of_futures_pairs': derivative_data.get('number_of_futures_pairs', 0),
                        'year_established': derivative_data.get('year_established', 0),
                        'country': derivative_data.get('country', ''),
                        'image': derivative_data.get('image', ''),
                        'url': derivative_data.get('url', '')
                    }
                )
            except requests.exceptions.HTTPError as e:
                print(f"Failed to import Derivative: {derivative}\nError: {e}")
            except Exception as e:
                print(f"Failed to import Derivative: {derivative}\nError: {e}")
