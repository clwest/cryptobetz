from django.core.management.base import BaseCommand
from cryptocurrencys.models import NFTS
import requests
from dotenv import load_dotenv
import os
load_dotenv()

coingecko = os.getenv('COINGECKO')


class Command(BaseCommand):
    help = 'Imports NFT data from an external API'

    def handle(self, *args, **options):
        url = 'https://pro-api.coingecko.com/api/v3/nfts/list'
        headers = {
            'Accepts': 'application/json',
            'X-CG-Pro-API-Key': coingecko
        }
        params = {'per_page': 200, 'page': 1}
        nfts = []

        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        nfts.extend(data)

        while len(data) == 200:
            params['page'] += 1
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            nfts.extend(data)

        print(f"Found {len(nfts)} NFTs")
        
        for nft in nfts:
            try:
                if 'status' in nft:
                    print(f"Failed to import NFT: {nft['status']['error_message']}")
                    continue

                url = f'https://pro-api.coingecko.com/api/v3/nfts/{nft["id"]}'
                response = requests.get(url, headers=headers)

                print(f"API response: {response.json()}")

                nft_data = response.json()

                if 'name' not in nft_data:
                    print(f"Failed to import NFT: {nft_data}")
                    continue

                nft_obj = NFTS.objects.create(
                    name=nft_data['name'],
                    contract_address=nft_data['contract_address'],
                    image_url=nft_data['image']['small'],
                    asset_platform=nft_data['asset_platform_id'],
                    native_currency=nft_data['native_currency'],
                    description=nft_data['description'],
                    total_supply=nft_data['total_supply'],
                    unique_address=nft_data['number_of_unique_addresses'],
                    market_cap=nft_data['market_cap']['usd'],
                    volume_24h=nft_data['volume_24h']['usd'],
                    floor_price=nft_data['floor_price']['usd'],
                )
            except Exception as e:
                print(f"Failed to import NFT: {nft}\nError: {e}")
