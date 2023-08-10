from django.db import models

# Create your models here.
class LiveAssetPrice(models.Model):
    
    gold_price = models.FloatField()
    silver_price = models.FloatField()
    copper_price = models.FloatField()
    platinum_price = models.FloatField()
    oil_price = models.FloatField()
    gas_price = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)