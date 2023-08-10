from django.contrib import admin
from . models import *

# Register your models here.
@admin.register(LiveAssetPrice)
class LiveAssetPriceAdmin(admin.ModelAdmin):
    list_display = (
    "gold_price", 
    "silver_price",
    "copper_price",
    "platinum_price",
    "oil_price",
    "gas_price",
    "timestamp"
    )