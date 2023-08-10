from rest_framework import serializers
from .models import *

class LiveAssetPriceserializer(serializers.Serializer):

    asset_name = serializers.CharField()
    timestamp_1 = serializers.DateTimeField()
    timestamp_2 = serializers.DateTimeField()

class FetchLiveAsset(serializers.Serializer):

    asset_name = serializers.CharField()
    timestamp = serializers.DateTimeField()