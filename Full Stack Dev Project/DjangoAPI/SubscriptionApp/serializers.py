from rest_framework import serializers 
from SubscriptionApp.models import Subscriptions

# Subscription Serializer 
class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = ('SubscriptionId','SubscriptionStockTicker','SubscriptionContactNumber')
