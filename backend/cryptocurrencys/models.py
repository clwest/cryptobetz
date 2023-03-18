from django.db import models
from django.utils.dateparse import parse_datetime
from datetime import date

# Create your models here.

class Cryptocurrency(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()
    symbol = models.CharField(max_length=100)
    categories = models.TextField()
    market_cap = models.FloatField()
    current_price = models.FloatField()
    total_volume = models.FloatField()
    circulating_supply = models.FloatField()
    total_supply = models.FloatField(null=True, blank=True)
    max_supply = models.FloatField(null=True, blank=True)
    price_change_percentage_24h = models.FloatField(null=True, blank=True)
    ath = models.FloatField()
    ath_date = models.DateField(null=True, blank=True)
    atl = models.FloatField()
    atl_date = models.DateField(null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    logo_url = models.URLField()
    website = models.URLField()
    twitter_handle = models.CharField(max_length=100,)
    reddit_url = models.URLField(null=True, blank=True)
    facebook_likes = models.IntegerField(null=True, blank=True)
    twitter_followers = models.IntegerField(null=True, blank=True)
    reddit_average_posts_48h = models.IntegerField(null=True, blank=True)
    reddit_average_comments_48h = models.IntegerField(null=True, blank=True)
    reddit_subscribers = models.IntegerField(null=True, blank=True)
    reddit_accounts_active_48h = models.IntegerField(null=True, blank=True)
    telegram_channel_user_count = models.IntegerField(null=True, blank=True)
    forks = models.IntegerField(null=True, blank=True)
    stars = models.IntegerField(null=True, blank=True)
    subscribers = models.IntegerField(null=True, blank=True)
    total_issues = models.IntegerField(null=True, blank=True)
    closed_issues = models.IntegerField(null=True, blank=True)
    pull_requests_merged = models.IntegerField(null=True, blank=True)
    pull_request_contributors = models.IntegerField(null=True, blank=True)
    code_additions = models.IntegerField(null=True, blank=True)
    code_deletions = models.IntegerField(null=True, blank=True)
    commit_count_4_weeks = models.IntegerField(null=True, blank=True)
    sentiment_votes_up_percentage = models.FloatField(null=True, blank=True)
    sentiment_votes_down_percentage = models.FloatField(null=True, blank=True)
    market_cap_rank = models.IntegerField(null=True, blank=True)
    coingecko_rank = models.IntegerField(null=True, blank=True)
    coingecko_score = models.FloatField(null=True, blank=True)
    developer_score = models.FloatField(null=True, blank=True)
    community_score = models.FloatField(null=True, blank=True)
    liquidity_score = models.FloatField(null=True, blank=True)
    public_interest_score = models.FloatField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.ath_date:
            self.ath_date = parse_datetime(self.ath_date).date().isoformat()
        if self.atl_date:
            self.atl_date = parse_datetime(self.atl_date).date().isoformat()
        if self.last_updated:
            self.last_updated = parse_datetime(self.last_updated).isoformat()
        super(Cryptocurrency, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class NFTS(models.Model):
    name = models.CharField(max_length=200)
    contract_address = models.CharField(max_length=255)
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

class Ticker(models.Model):
    base = models.CharField(max_length=200)
    target = models.CharField(max_length=200)
    market_name = models.CharField(max_length=200)
    market_identifier = models.CharField(max_length=200)
    has_trading_incentive = models.BooleanField()
    last = models.DecimalField(max_digits=20, decimal_places=10)
    volume = models.DecimalField(max_digits=20, decimal_places=10)
    converted_last_btc = models.DecimalField(max_digits=20, decimal_places=10)
    converted_last_eth = models.DecimalField(max_digits=20, decimal_places=10)
    converted_last_usd = models.DecimalField(max_digits=20, decimal_places=10)
    converted_volume_btc = models.DecimalField(max_digits=20, decimal_places=10)
    converted_volume_eth = models.DecimalField(max_digits=20, decimal_places=10)
    converted_volume_usd = models.DecimalField(max_digits=20, decimal_places=10)
    trust_score = models.CharField(max_length=200)
    bid_ask_spread_percentage = models.DecimalField(max_digits=10, decimal_places=5)
    timestamp = models.DateTimeField()
    last_traded_at = models.DateTimeField()
    last_fetch_at = models.DateTimeField()
    is_anomaly = models.BooleanField()
    is_stale = models.BooleanField()
    trade_url = models.URLField()
    token_info_url = models.URLField(null=True)
    coin_id = models.CharField(max_length=200)
    
class Exchange(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()
    twitter_handle = models.CharField(max_length=200)
    telegram_url = models.CharField(max_length=200, null=True)
    centralized = models.BooleanField()
    trust_score = models.IntegerField()
    trust_score_rank = models.IntegerField()
    trade_volume_24h_btc = models.DecimalField(max_digits=20, decimal_places=10)
    trade_volume_24h_btc_normalized = models.DecimalField(max_digits=20, decimal_places=10)
    tickers = models.ManyToManyField(Ticker, related_name='exchanges')
    
class Index(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    constituents = models.ManyToManyField(Cryptocurrency)

class Derivative(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    underlying_asset = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    volume_24h = models.DecimalField(max_digits=20, decimal_places=10)
    price = models.DecimalField(max_digits=20, decimal_places=10)
    open_interest = models.DecimalField(max_digits=20, decimal_places=10)
    last_traded_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    

class Companies(models.Model):
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    total_holdings = models.DecimalField(max_digits=20, decimal_places=10)
    total_entry_value_usd = models.DecimalField(max_digits=20, decimal_places=10)
    total_current_value_usd = models.DecimalField(max_digits=20, decimal_places=10)
    percentage_of_total_supply = models.DecimalField(max_digits=10, decimal_places=5)