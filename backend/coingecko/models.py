from django.db import models
from django.utils.dateparse import parse_datetime
from datetime import date, datetime

# Create your models here.
class CoinCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name

class CoinPlatform(models.Model):
    name = models.CharField(max_length=255, unique=True)
    platform_id = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name


class Coin(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()
    symbol = models.CharField(max_length=100)
    asset_platform_id = models.CharField(max_length=100, null=True, blank=True)
    logo_url = models.URLField() 
    url = models.URLField()
    categories = models.ManyToManyField(CoinCategory, related_name="coins")
    platform = models.ForeignKey(CoinPlatform, related_name="coins", null=True, on_delete=models.CASCADE)
    sentiment_votes_up_percentage = models.FloatField(null=True, blank=True)
    sentiment_votes_down_percentage = models.FloatField(null=True, blank=True)
    coingecko_rank = models.IntegerField(null=True, blank=True)
    coingecko_score = models.FloatField(null=True, blank=True)
    liquidity_score = models.FloatField(null=True, blank=True)
    public_interest_score = models.FloatField(null=True, blank=True)
    



class CoinMarketData(models.Model):
    coin = models.OneToOneField(Coin, on_delete=models.CASCADE, primary_key=True)
    current_price = models.FloatField() # only USD
    total_value_locked_btc = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    total_value_locked_usd = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    ath = models.FloatField()
    ath_date = models.DateField(null=True, blank=True)
    atl = models.FloatField()
    atl_date = models.DateField(null=True, blank=True)
    market_cap = models.DecimalField(max_digits=20, decimal_places=8, null=True)
    market_cap_rank = models.IntegerField(null=True, blank=True)
    fully_diluted_valuation = models.FloatField()    
    total_volume = models.FloatField()
    high_24h = models.FloatField()
    low_24h = models.FloatField()
    circulating_supply = models.FloatField()    
    last_updated = models.DateTimeField(null=True, blank=True)
    max_supply = models.FloatField(null=True, blank=True) 
    price_change_24h = models.FloatField()   
    price_change_percentage_24h = models.FloatField(null=True, blank=True)
    price_change_percentage_1h = models.FloatField(null=True, blank=True)
    price_change_percentage_7d = models.FloatField(null=True, blank=True)
    price_change_percentage_14d = models.FloatField(null=True, blank=True)
    price_change_percentage_30d = models.FloatField(null=True, blank=True)
    price_change_percentage_60d = models.FloatField(null=True, blank=True)
    price_change_percentage_200d = models.FloatField(null=True, blank=True)
    price_change_percentage_1y = models.FloatField(null=True, blank=True)
    total_supply = models.FloatField(null=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        if self.ath_date:
            self.ath_date = parse_datetime(self.ath_date).date().isoformat()
        if self.atl_date:
            self.atl_date = parse_datetime(self.atl_date).date().isoformat()
        if self.last_updated:
            self.last_updated = parse_datetime(self.last_updated).isoformat()
        super(CoinMarketData, self).save(*args, **kwargs)

    def __str__(self):
        return self.name 


class HomepageURL(models.Model):
    url = models.URLField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.url

class BlockchainSiteURL(models.Model):
    url = models.URLField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.url


class CoinCommunityData(models.Model):
    coin = models.OneToOneField(Coin, on_delete=models.CASCADE, primary_key=True, related_name='community_data')
    homepage = models.ManyToManyField(HomepageURL,  related_name="coins")
    blockchain_site = models.ManyToManyField(BlockchainSiteURL,  related_name="coins")
    chat_url = models.URLField(max_length=255, null=True, blank=True)
    twitter_screen_name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    twitter_followers = models.IntegerField(null=True, blank=True)
    telegram_channel_identifier = models.CharField(max_length=255, unique=True, null=True, blank=True)
    telegram_channel_user_count = models.IntegerField(null=True, blank=True)
    community_score = models.FloatField(null=True, blank=True)
        
    def __str__(self):
        return f"{self.coin.name} Community Data"



class CoinDeveloperData(models.Model):
    description = models.TextField(null=True, blank=True, verbose_name='Developer Data')
    coin = models.OneToOneField(Coin, on_delete=models.CASCADE, primary_key=True, related_name='developer_data')
    forks = models.IntegerField(null=True, blank=True, verbose_name="Forks")
    stars = models.IntegerField(null=True, blank=True, verbose_name="Stars")
    subscribers = models.IntegerField(null=True, blank=True, verbose_name="Subscribers")
    total_issues = models.IntegerField(null=True, blank=True, verbose_name="Total Issues")
    closed_issues = models.IntegerField(null=True, blank=True, verbose_name="Closed Issues")
    pull_requests_merged = models.IntegerField(null=True, blank=True, verbose_name="Pull Requests")
    pull_request_contributors = models.IntegerField(null=True, blank=True, verbose_name="Pull Requests Contributors")
    code_additions = models.IntegerField(null=True, blank=True, verbose_name="Code Additions")
    code_deletions = models.IntegerField(null=True, blank=True, verbose_name="Code Deletions")
    commit_count_4_weeks = models.IntegerField(null=True, blank=True, verbose_name="Commit Count (4 weeks)")
    developer_score = models.FloatField(null=True, blank=True, verbose_name="Developer Score")
    repos_url = models.JSONField(default=list, null=True, blank=True)
    def __str__(self):
        return f"{self.coin.name} Developer Data"
    
    class Meta:
        verbose_name = "Developer Data"


class Exchange(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True, verbose_name='Description')
    url = models.URLField()
    twitter_handle = models.CharField(max_length=500, null=True)
    facebook_url = models.URLField(max_length=500, null=True)
    telegram_url = models.URLField(max_length=500, null=True)
    centralized = models.BooleanField()
    trust_score = models.IntegerField(null=True, default=0)
    trust_score_rank = models.IntegerField(null=True, default=0)
    trade_volume_24h_btc = models.DecimalField(max_digits=20, decimal_places=10)
    trade_volume_24h_btc_normalized = models.DecimalField(max_digits=20, decimal_places=10)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Exchange'
        verbose_name_plural = 'Exchanges'


class Ticker(models.Model):
    base = models.CharField(max_length=200)
    target = models.CharField(max_length=200)
    market_name = models.CharField(max_length=200)
    has_trading_incentive = models.BooleanField()
    last = models.DecimalField(max_digits=20, decimal_places=10)
    volume = models.DecimalField(max_digits=20, decimal_places=10)
    converted_last_btc = models.DecimalField(max_digits=20, decimal_places=10)
    converted_last_eth = models.DecimalField(max_digits=20, decimal_places=18)
    converted_last_usd = models.DecimalField(max_digits=20, decimal_places=10)
    converted_volume_btc = models.DecimalField(max_digits=20, decimal_places=10)
    converted_volume_eth = models.DecimalField(max_digits=20, decimal_places=10)
    converted_volume_usd = models.DecimalField(max_digits=20, decimal_places=10)
    trust_score = models.CharField(max_length=200, null=True, blank=True)
    bid_ask_spread_percentage = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)
    timestamp = models.DateTimeField()
    last_traded_at = models.DateTimeField()
    last_fetch_at = models.DateTimeField()
    trade_url = models.URLField(null=True, blank=True)
    token_info_url = models.URLField(null=True, blank=True)
    target_coin_id = models.CharField(max_length=200, null=True, blank=True)
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, null=True, blank=True)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        unique_together = ('coin', 'exchange')

    def __str__(self):
        return self.market_name
    
class Index(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    constituents = models.ManyToManyField(Coin)

class Derivative(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    underlying_asset = models.ForeignKey(Coin, on_delete=models.CASCADE, null=True, blank=True, related_name='derivatives')
    open_interest_btc = models.DecimalField(max_digits=30, decimal_places=20, null=True, blank=True)
    volume_24h = models.DecimalField(max_digits=20, decimal_places=10)
    number_of_perpetual_pairs = models.IntegerField(null=True, blank=True)
    number_of_futures_pairs = models.IntegerField(null=True)
    image = models.URLField(null=True)
    country = models.CharField(max_length=50, null=True)
    year_established = models.DateTimeField(auto_now_add=True)
    url = models.URLField(null=True)

class NewCoin(models.Model):
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=10, unique=True, db_index=True)
    coingecko_id = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "New Coins"
        
        
    def __str__(self):
        return self.name

class NFTS(models.Model):
    name = models.CharField(max_length=200)
    contract_address = models.CharField(max_length=255, null=True)
    image_url = models.URLField()
    asset_platform = models.CharField(max_length=50)
    native_currency = models.CharField(max_length=50)
    description = models.TextField()
    total_supply = models.FloatField(null=True, blank=True)
    unique_address = models.FloatField(null=True, blank=True)
    market_cap = models.FloatField()
    volume_24h = models.FloatField()
    floor_price = models.FloatField()

    def __str__(self):
        return self.name
