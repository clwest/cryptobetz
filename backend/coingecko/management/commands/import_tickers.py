from django.core.management.base import BaseCommand
from coingecko.models import Ticker
import requests
from dotenv import load_dotenv
from decimal import Decimal
import os
load_dotenv()

coingecko = os.getenv('COINGECKO')


class Command(BaseCommand):
    help = 'Imports Tickers data from an external API'

    def handle(self, *args, **options):
        url = 'https://pro-api.coingecko.com/api/v3/coins/list'
        headers = {
            'Accepts': 'application/json',
            'X-CG-Pro-API-Key': coingecko
        }
        params = {'per_page': 200, 'page': 1}
        tickers = []

        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        tickers.extend(data)

        while len(data) == 200:
            params['page'] += 1
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            tickers.extend(data)

        print(f"Found {len(tickers)} Tickers")
        
        for ticker in tickers:
            try:
                if Ticker.objects.filter(market_name=ticker['name']).exists():
                    print(f"Ticker already exists: {ticker['name']}")
                    continue

                url = f'https://pro-api.coingecko.com/api/v3/coins/{ticker["id"]}/tickers'
                response = requests.get(url, headers=headers)

                ticker_data = response.json()

                if not ticker_data['tickers']:
                    print(f"No tickers found for coin ID: {ticker['id']}")
                    continue
                
                # Skip if target_coin_id is missing
                if 'target_coin_id' not in ticker_data['tickers'][0]:
                    print(f"Skipping Ticker with missing target_coin_id: {ticker['name']}")
                    continue

                # Truncate values to avoid numeric field overflow
                def truncate(value, precision=20, scale=10):
                    factor = 10 ** scale
                    return round(Decimal(value) * Decimal(factor)) / Decimal(factor)

                ticker_defaults={
                    'market_name': ticker_data['tickers'][0]['market']['name'],
                    'base': ticker_data['tickers'][0]['base'],
                    'target': ticker_data['tickers'][0]['target'],
                    'has_trading_incentive': ticker_data['tickers'][0]['market']['has_trading_incentive'],
                    'last': ticker_data['tickers'][0]['last'],
                    'volume': ticker_data['tickers'][0]['volume'],
                    'converted_last_btc': ticker_data['tickers'][0]['converted_last']['btc'],
                    'converted_last_eth': ticker_data['tickers'][0]['converted_last']['eth'],
                    'converted_last_usd': ticker_data['tickers'][0]['converted_last']['usd'],
                    'converted_volume_btc': ticker_data['tickers'][0]['converted_volume']['btc'],
                    'converted_volume_eth': ticker_data['tickers'][0]['converted_volume']['eth'],
                    'converted_volume_usd': ticker_data['tickers'][0]['converted_volume']['usd'],
                    'trust_score': ticker_data['tickers'][0]['trust_score'],
                    'bid_ask_spread_percentage': ticker_data['tickers'][0]['bid_ask_spread_percentage'],
                    'timestamp': ticker_data['tickers'][0]['timestamp'],
                    'last_traded_at': ticker_data['tickers'][0]['last_traded_at'],
                    'last_fetch_at': ticker_data['tickers'][0]['last_fetch_at'],
                    'is_anomaly': ticker_data['tickers'][0]['is_anomaly'],
                    'trade_url': ticker_data['tickers'][0]['trade_url'],
                    'token_info_url': ticker_data['tickers'][0]['token_info_url'],
                    'target_coin_id': ticker_data['tickers'][0]['target_coin_id'],
                    }
                try:
                   Ticker.objects.create(**{'market_name': ticker_data['tickers'][0]['market']['name'], **ticker_defaults})
                except Exception as e:
                    if 'numeric field overflow' in str(e):
                        print(f"Skipping Ticker due to numeric field overflow: {ticker['name']}")
                    else:
                        print(f"Failed to create Ticker: {ticker}\nError: {e}")
                
            except Exception as e:
                print(f"Failed to import Ticker: {ticker}\nError: {e}")