import requests
from django.shortcuts import render
from django_q.models import Schedule
from django_q.tasks import schedule
from django.db.models import F
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import *
from .serializers import *

ASSET_FIELDS = {
            'gold': 'gold_price',
            'silver': 'silver_price',
            'copper': 'copper_price',
            'platinum': 'platinum_price',
            'oil': 'oil_price',
            'gas': 'gas_price',
        }

# Create your views here.
def fetch_live_price_data():

    # base_url = settings.COMMODITIES_BASE_URL
    # endpoint = settings.ENDPOINT
    # params = {
    #     "access_key": settings.COMMODITIES_API_KEY,
    #     "base": settings.BASE,
    #     "symbols": settings.SYMBOLS
    # }
    # headers = {
    #     "Content-Type": "application/json"
    # }

    response = requests.get("https://mocki.io/v1/42e31653-b228-45ea-8400-bf590cdd116f")
    # response = requests.get(f'{base_url}{endpoint}', params=params, headers=headers)
    data = response.json()
    data = data['data']['rates']

    LiveAssetPrice.objects.create(
        gold_price=data.get('XAU'),
        silver_price=data.get('XAG'),
        copper_price=data.get('XCU'),
        platinum_price=data.get('XPT'),
        oil_price=data.get('BRENTOIL'),
        gas_price=data.get('NG')
        )
    
# schedule('dump.views.fetch_live_price_data', schedule_type=Schedule.MINUTES, hour=1)


class AssetLivePriceViewset(ModelViewSet):

    queryset = LiveAssetPrice.objects.all()
    serializer_class = LiveAssetPriceserializer
    http_method_names = ['post']


    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        asset_name = request.data.get('asset_name')
        asset_field=ASSET_FIELDS.get(asset_name)
        if not asset_field:
            return Response({"error":"Invalid asset name!!"})
        
        timestamp_1 = request.data.get('timestamp_1')
        timestamp_2 = request.data.get('timestamp_2')

        print(asset_field)
        live_asset_prices = LiveAssetPrice.objects.filter(timestamp__range=[timestamp_1,timestamp_2]).annotate(price=F(asset_field)).values('price','timestamp')


        return Response(list(live_asset_prices), status=status.HTTP_200_OK)

