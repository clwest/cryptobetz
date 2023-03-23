from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework import filters, generics, pagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_datetime
from datetime import date, datetime
from .models import Coin, Exchange, Derivative, Ticker, NewCoin, NFTS
from .serializers import CoinSerializer, ExchangeSerializer, DerivativeSerializer, TickerSerializer, NewCoinSerializer, NFSerializer

class CoinPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CoinFilter(filters.FilterSet):
    class Meta:
        model = Coin
        fields = {
            'name': ['exact', 'icontains'],
            'symbol': ['exact', 'icontains'],
            'price': ['exact', 'lt', 'gt'],
        }

class CoinList(generics.ListAPIView):
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer
    pagination_class = CoinPagination
    filterset_class = CoinFilter
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['name', 'symbol', 'price']

class CoinDetail(generics.RetrieveAPIView, generics.UpdateAPIView):
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer
    
    def put(self, request, *args, **kwargs):
        coin = self.get_object()
        serializer = CoinSerializer(coin, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExchangeList(generics.ListAPIView):
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['name', 'country']
    ordering_fields = ['name', 'volume_24h', 'trust_score']
    ordering = ['-volume_24h']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExchangeDetail(generics.RetrieveAPIView):
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            return Response({'error': 'Exchange not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class DerivativeFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    country = filters.CharFilter(lookup_expr='icontains')
    year_established = filters.NumberFilter()

    class Meta:
        model = Derivative
        fields = ['name', 'country', 'year_established']

class DerivativeList(generics.ListAPIView):
    queryset = Derivative.objects.all()
    serializer_class = DerivativeSerializer
    filterset_class = DerivativeFilter

class DerivativeDetail(generics.RetrieveAPIView):
    queryset = Derivative.objects.all()
    serializer_class = DerivativeSerializer


class TickerList(generics.ListAPIView):
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer
    pagination_class = CoinPagination

    def get_queryset(self):
        queryset = Ticker.objects.all()

        # Filter by base currency
        base = self.request.query_params.get('base', None)
        if base is not None:
            queryset = queryset.filter(base=base)

        # Filter by target currency
        target = self.request.query_params.get('target', None)
        if target is not None:
            queryset = queryset.filter(target=target)

        # Filter by market name
        market_name = self.request.query_params.get('market_name', None)
        if market_name is not None:
            queryset = queryset.filter(market_name=market_name)

        return queryset


class TickerDetail(generics.RetrieveAPIView):
    queryset = Ticker.objects.all()
    serializer_class = TickerSerializer

    def get(self, request, *args, **kwargs):
        ticker = self.get_object()
        data = self.get_serializer(ticker).data

        # Include historical price data
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

                if start_date > end_date:
                    return Response({'error': 'start_date must be earlier than end_date'}, status=status.HTTP_400_BAD_REQUEST)

                historical_data = ticker.historical_prices.filter(date__range=(start_date, end_date)).values('date', 'price')
                data['historical_prices'] = historical_data
            except ValueError:
                return Response({'error': 'Invalid date format, use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data)


class NewCoinPagination(pagination.PageNumberPagination):
    page_size = 50


class NewCoinList(generics.ListAPIView):
    queryset = NewCoin.objects.all()
    serializer_class = NewCoinSerializer
    pagination_class = NewCoinPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'symbol', 'coingecko_id']
    ordering_fields = ['name', 'symbol', 'coingecko_id']
    ordering = ['name']

class NewCoinDetail(generics.RetrieveAPIView):
    queryset = NewCoin.objects.all()
    serializer_class = NewCoinSerializer

    def get_object(self):
        try:
            obj = self.queryset.get(coingecko_id=self.kwargs['pk'])
        except NewCoin.DoesNotExist:
            raise NotFound()
        self.check_object_permissions(self.request, obj)
        return obj

class NFTList(generics.ListAPIView):
    queryset = NFTS.objects.all()
    serializer_class = NFSerializer
    pagination_class = CoinPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = {
        'name': ['exact', 'icontains'],
        'market_cap': ['exact', 'gte', 'lte'],
        'volume_24h': ['exact', 'gte', 'lte'],
        # add more fields here for filtering
    }
    ordering_fields = ['name', 'market_cap', 'volume_24h']
    search_fields = ['name', 'description']

class NFTDetail(generics.RetrieveAPIView):
    queryset = NFTS.objects.all()
    serializer_class = NFSerializer
    pagination_class = CoinPagination

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except NFTS.DoesNotExist:
            raise NotFound("NFT not found")
        serializer = self.get_serializer(instance)
        return Response(serializer.data)