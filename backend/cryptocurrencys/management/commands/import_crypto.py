from django.core.management.base import BaseCommand
from cryptocurrencys.models import Cryptocurrency
import requests
from dotenv import load_dotenv
import os
load_dotenv()

coingecko = os.getenv('COINGECKO')

class Command(BaseCommand):
    help = "Fetches cryptocurrency data and stores it in the database"
    
    def handle(self, *args, **options):
          url = 'https://pro-api.coingecko.com/api/v3/coins/list'
          headers = {
              'Accepts': 'application/json',
              'X-CG-Pro-API-Key': coingecko
          }
          params = {'per_page': 200, 'page': 1}
          coins = []

          response = requests.get(url, headers=headers, params=params)
          data = response.json()
          coins.extend(data)

          while len(data) == 200:
              params['page'] += 1
              response = requests.get(url, headers=headers, params=params)
              data = response.json()
              coins.extend(data)
          
          for coin in coins:
              url = f'https://api.coingecko.com/api/v3/coins/{coin["id"]}'
              response = requests.get(url, headers=headers)
              
              try:
                if 'status' in coin:
                    print(f"Failed to import Coin: {coin['status']['error_message']}")
                    continue

                url = f'https://pro-api.coingecko.com/api/v3/coins/{coin["id"]}'
                response = requests.get(url, headers=headers)

                # print(f"API response: {response.json()}")
                
                coin_data = response.json()

                if 'name' not in coin_data:
                    print(f"Failed to import Coin: {coin_data}")
                    continue
                    
                coin_object = Cryptocurrency.objects.create(
                          name=coin_data['name'],
                          description=coin_data['description']['en'],
                          symbol=coin_data['symbol'],
                          categories=coin_data['categories'],
                          market_cap=coin_data['market_data']['market_cap']['usd'],
                          current_price=coin_data['market_data']['current_price']['usd'],
                          total_volume=coin_data['market_data']['total_volume']['usd'],
                          circulating_supply=coin_data['market_data']['circulating_supply'],
                          total_supply=coin_data['market_data']['total_supply'],
                          max_supply=coin_data['market_data']['max_supply'],
                          price_change_percentage_24h=coin_data['market_data']['price_change_percentage_24h'],
                          ath=coin_data['market_data']['ath']['usd'],
                          ath_date=coin_data['market_data']['ath_date']['usd'],
                          atl=coin_data['market_data']['atl']['usd'],
                          atl_date=coin_data['market_data']['atl_date']['usd'],
                          last_updated=coin_data['last_updated'],
                          logo_url=coin_data['image']['large'],
                          website=coin_data['links']['homepage'][0],
                          twitter_handle=coin_data['links']['twitter_screen_name'],
                          reddit_url=coin_data['links']['subreddit_url'],
                          facebook_likes=coin_data['community_data']['facebook_likes'],
                          twitter_followers=coin_data['community_data']['twitter_followers'],
                          reddit_average_posts_48h=coin_data['community_data']['reddit_average_posts_48h'],
                          reddit_average_comments_48h=coin_data['community_data']['reddit_average_comments_48h'],
                          reddit_subscribers=coin_data['community_data']['reddit_subscribers'],
                          reddit_accounts_active_48h=coin_data['community_data']['reddit_accounts_active_48h'],
                          telegram_channel_user_count=coin_data['community_data']['telegram_channel_user_count'],
                          forks=coin_data['developer_data']['forks'],
                          stars=coin_data['developer_data']['stars'],
                          subscribers=coin_data['developer_data']['subscribers'],
                          total_issues=coin_data['developer_data']['total_issues'],
                          closed_issues=coin_data['developer_data']['closed_issues'],
                          pull_requests_merged=coin_data['developer_data']['pull_requests_merged'],
                          pull_request_contributors=coin_data['developer_data']['pull_request_contributors'],
                          code_additions=coin_data['developer_data']['code_additions_deletions_4_weeks']['additions'],
                          code_deletions=coin_data['developer_data']['code_additions_deletions_4_weeks']['deletions'],
                          commit_count_4_weeks=coin_data['developer_data']['commit_count_4_weeks'],
                          sentiment_votes_up_percentage=coin_data['sentiment_votes_up_percentage'],
                          sentiment_votes_down_percentage=coin_data['sentiment_votes_down_percentage'],
                          market_cap_rank=coin_data['market_cap_rank'],
                          coingecko_rank=coin_data['coingecko_rank'],
                          coingecko_score=coin_data['coingecko_score'],
                          developer_score=coin_data['developer_score'],
                          community_score=coin_data['community_score'],
                          liquidity_score=coin_data['liquidity_score'],
                          public_interest_score=coin_data['public_interest_score'],
                      )
              except Exception as e:
                print(f"Failed to import Coin: {coin}\nError: {e}")