from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from decimal import Decimal
from datetime import datetime
from .models import Coin
from .serializers import CoinSerializer

class CoinListTest(APITestCase):
    def setUp(self):
        Coin.objects.create(name="Bitcoin", symbol="BTC", price=Decimal('59487.09'), market_cap=Decimal('1113291094009'), volume_24h=Decimal('45884547022'), price_change_24h=Decimal('-0.12'), price_change_percentage_24h=Decimal('-0.0002'), last_updated=datetime.now())
        Coin.objects.create(name="Ethereum", symbol="ETH", price=Decimal('1804.18'), market_cap=Decimal('207537792819'), volume_24h=Decimal('27137203199'), price_change_24h=Decimal('0.27'), price_change_percentage_24h=Decimal('0.0002'), last_updated=datetime.now())
        Coin.objects.create(name="Binance Coin", symbol="BNB", price=Decimal('282.83'), market_cap=Decimal('43752565513'), volume_24h=Decimal('4787843019'), price_change_24h=Decimal('-0.35'), price_change_percentage_24h=Decimal('-0.0001'), last_updated=datetime.now())
        
    def test_error_handling(self):
        url = reverse('coin-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_pagination(self):
        url = reverse('coin-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, {'page': 1, 'page_size': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filtering(self):
        url = reverse('coin-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, {'name': 'Bitcoin'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_ordering(self):
        url = reverse('coin-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, {'ordering': 'price'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], 'Ethereum')

    def test_list_coins(self):
        url = reverse('coin-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Bitcoin')

    def test_get_all_coins(self):
        url = reverse('coin-list')
        response = self.client.get(url)
        coins = Coin.objects.all()
        serializer = CoinSerializer(coins, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


    def test_filter_by_name(self):
        url = reverse('coin-list')
        response = self.client.get(url, {'name': 'bitcoin'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Bitcoin')

    def test_filter_by_symbol(self):
        url = reverse('coin-list')
        response = self.client.get(url, {'symbol': 'btc'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['symbol'], 'BTC')

    def test_filter_by_price(self):
        url = reverse('coin-list')
        response = self.client.get(url, {'price__lt': 70000})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['price'], '60000.00')

    def test_order_by_name(self):
        url = reverse('coin-list')
        response = self.client.get(url, {'ordering': 'name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Bitcoin')
