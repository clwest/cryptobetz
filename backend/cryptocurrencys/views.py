from django.shortcuts import render
from django.http import HttpResponse
from .models import Cryptocurrency
from .cryptocurrency import get_coins_data

def update_cryptocurrencies(request):
    cryptocurrencies = get_coins_data()
    for currency in cryptocurrencies:
        Cryptocurrency.objects.update_or_create(name=currency['name'], defaults=currency)
    return HttpResponse('Cryptocurrencies updated successfully!')
