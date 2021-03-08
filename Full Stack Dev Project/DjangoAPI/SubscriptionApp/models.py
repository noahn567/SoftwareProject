from django.db import models

# Subscription Model
class Subscriptions(models.Model):
    SubscriptionId = models.AutoField(primary_key=True)
    SubscriptionStockTicker = models.CharField(max_length=20)
    SubscriptionContactNumber = models.CharField(max_length=20)

