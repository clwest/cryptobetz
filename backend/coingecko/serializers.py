from rest_framework import serializers
from .models import Coin, Exchange, Derivative, Ticker, NewCoin, NFTS


class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ['id', 'name', 'symbol', 'image', 'price', 'market_cap', 'volume_24h', 'price_change_24h', 'price_change_percentage_24h']


class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = ('name', 'country')


class DerivativeSerializer(serializers.ModelSerializer):
    exchange = serializers.StringRelatedField()
    base_asset = serializers.StringRelatedField()
    target_asset = serializers.StringRelatedField()

    class Meta:
        model = Derivative
        fields = ['id', 'name', 'exchange', 'base_asset', 'target_asset', 'contract_type', 'settlement_period', 'tick_size', 'lot_size', 'price', 'volume_24h']
        read_only_fields = ['id', 'exchange', 'base_asset', 'target_asset']


class TickerSerializer(serializers.ModelSerializer):
    market_name = serializers.SerializerMethodField()

    class Meta:
        model = Ticker
        fields = ['id', 'base', 'target', 'last_price', 'volume', 'timestamp', 'market_name']

    def get_market_name(self, obj):
        return f"{obj.base.upper()}/{obj.target.upper()}"


class NewCoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewCoin
        fields = ['name', 'symbol']


class NFTSSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFTS
        fields = '__all__'
