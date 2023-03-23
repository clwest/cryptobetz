from django.core.management.base import BaseCommand
import logging
from django.db import IntegrityError
from coingecko.models import Coin, CoinCategory, CoinPlatform, CoinDeveloperData, CoinMarketData, HomepageURL, BlockchainSiteURL, CoinCommunityData 
import requests
from dotenv import load_dotenv
import os
load_dotenv()

coingecko = os.getenv('COINGECKO')
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Fetches Coin data and stores it in the database"
    
    def handle(self, *args, **options):
            url = 'https://pro-api.coingecko.com/api/v3/coins/list'
            headers = {
                'Accepts': 'application/json',
                'X-CG-Pro-API-Key': coingecko
            }
            params = {'per_page': 200, 'page': 1}
            coins = []

            while True:
                response = requests.get(url, headers=headers, params=params)
                data = response.json()
                coins.extend(data)
                if len(data) < 200:
                    break
                params["page"] += 1
                
                
            coin_market_data_list = []
            coin_developer_data_list = []
            coin_community_data_list = []
            
            for coin in coins:
                try:
                    # Check to see if coin is in database
                    if Coin.objects.filter(name=coin['name']).exists():
                        logger.info(f"Coin already exists: {coin_data['name']}")
                        continue
                    
                    url = f'https://pro-api.coingecko.com/api/v3/coins/{coin["id"]}'
                    response = requests.get(url, headers=headers)
                    coin_data = response.json()
                    
                    if 'name' not in coin_data or 'market_data' not in coin_data:
                        logger.warning(f"Failed to import Coin: {coin_data}")
                        continue

                    market_data = coin_data['market_data']
                    links = coin_data['links']
                    developer_data = coin_data['developer_data']
                    community_data = coin_data['community_data']
                    
                    blockchain_site_url=BlockchainSiteURL.objects.create(url=coin_data['links']['blockchain_site'][0]) if coin_data.get('links', {}).get('blockchain_site') else None
                    homepage_url=HomepageURL.objects.create(url=coin_data['links']['homepage'][0]) if coin_data.get('links', {}).get('homepage') else None
                    
                    
                    if 'usd' not in market_data['market_cap']:
                        logger.warning(f"Failed to import Coin: {coin_data}")
                    
                    # Create the coin object
                    categories = [CoinCategory(name=category) for category in coin_data.get("categories", [])
                    ]
                    CoinCategory.objects.bulk_create(categories)

                    platforms = [CoinPlatform(name=platform, url=platforms[platform]) for platform in coin_data.get("platforms", {})
                    ]
                    CoinPlatform.objects.bulk_create(platforms)
                    
                    try:
                    
                        coin_object = Coin.objects.create(
                            name=coin_data['name'],
                            contract_address=coin_data['contract_address'],
                            description=coin_data['description']['en'],
                            symbol=coin_data['symbol'],
                            asset_platform_id=coin_data['asset_platform_id'],
                            logo_url=coin_data['image']['small'],
                            coingecko_rank=coin_data['coingecko_rank'],
                            coingecko_score=coin_data['coingecko_score'],
                            sentiment_votes_up_percentage=coin_data['sentiment_votes_up_percentage'],
                            sentiment_votes_down_percentage=coin_data['sentiment_votes_down_percentage'],
                            liquidity_score=coin_data['liquidity_score'],
                            public_interest_score=coin_data['public_interest_score'],
                            last_updated=coin_data['last_updated'],
                        )
                    
                    except IntegrityError as e:
                        logger.warning(f"Failed to create coin object for {coin_data['name']}, Error: {str(e)}")

                    coin_object.categories.set(categories)
                    coin_object.platforms.set(platforms)
                        
                        
                    # Create market data
                    coin_market_data = CoinMarketData(
                        coin=coin_object,
                        current_price=market_data['current_price']['usd'],
                        market_cap=market_data['market_cap']['usd'],
                        total_value_locked_btc=market_data['total_value_locked']['btc'],
                        total_value_locked_usd=market_data['total_value_locked']['usd'],
                        ath=market_data['ath']['usd'],
                        ath_date=market_data['ath_date']['usd'],
                        atl=market_data['atl']['usd'],
                        atl_date=market_data['atl_date']['usd'],
                        market_cap_rank=market_data['market_cap_rank'],
                        fully_diluted_valuation = market_data['fully_diluted_valuation'],
                        total_volume=market_data['total_volume']['usd'],
                        high_24h=market_data['high_24h'],
                        low_24h=market_data['low_24h'],
                        circulating_supply=market_data['circulating_supply'],
                        last_updated=market_data['last_updated'],
                        max_supply=market_data['max_supply'],
                        price_change_24h=market_data['price_change_24h'],
                        price_change_percentage_24h=market_data['price_change_percentage_24h'],
                        price_change_percentage_1h=market_data['price_change_percentage_1h'],
                        price_change_percentage_7d=market_data['price_change_percentage_7d'],
                        price_change_percentage_14d=market_data['price_change_percentage_14d'],
                        price_change_percentage_30d=market_data['price_change_percentage_30d'],
                        price_change_percentage_60d=market_data['price_change_percentage_60d'],
                        price_change_percentage_200d=market_data['price_change_percentage_200d'],
                        price_change_percentage_1y=market_data['price_change_percentage_1y'],
                        total_supply=market_data['total_supply'],
                    )
                    coin_market_data_list.append(coin_market_data)
                        
                    coin_developer_data = CoinDeveloperData(
                        coin=coin_object,
                        forks=developer_data['forks'],
                        stars=developer_data['stars'],
                        subscribers=developer_data['subscribers'],
                        total_issues=developer_data['total_issues'],
                        closed_issues=developer_data['closed_issues'],
                        pull_requests_merged=developer_data['pull_requests_merged'],
                        pull_request_contributors=developer_data['pull_request_contributors'],
                        code_additions=developer_data['code_additions_deletions_4_weeks']['additions'],
                        code_deletions=developer_data['code_additions_deletions_4_weeks']['deletions'],
                        commit_count_4_weeks=developer_data['commit_count_4_weeks'],
                        developer_score=coin_data['developer_score'],
                        repos_url = links['repos_url'],
                    )
                    coin_developer_data_list.append(coin_developer_data)
                    
                    coin_community_data = CoinCommunityData(
                        coin=coin_object,
                        twitter_handle=links['twitter_screen_name'],
                        telegram_channel_identifier=links['telegram_channel_identifier'],
                        twitter_followers=community_data['twitter_followers'],
                        telegram_channel_user_count=community_data['telegram_channel_user_count'],
                        chat_url=links['chat_url'],
                        community_score=coin_data['community_score'],
                        homepage_url=homepage_url,
                        blockchain_site_url=blockchain_site_url,
                        
                    )
                    coin_community_data_list.append(coin_community_data)
                    
                except Exception as e:
                    print(f"Failed to import coin {coin['name']}. Error: {str(e)}")
                
            try:
                CoinCommunityData.objects.bulk_create(coin_community_data_list)
            except IntegrityError as e:
                logger.warning("Failed to bulk create CoinCommunityData objects: {}".format(str(e)))
            try:
                CoinDeveloperData.objects.bulk_create(coin_developer_data_list)
            except IntegrityError as e:
                logger.warning("Failed to bulk create CoinDeveloperData objects: {}".format(str(e)))
            try:
                CoinMarketData.objects.bulk_create(coin_market_data_list)
            except IntegrityError as e:
                logger.warning("Failed to bulk create CoinMarketData objects: {}".format(str(e)))