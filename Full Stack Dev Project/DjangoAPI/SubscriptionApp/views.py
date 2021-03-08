from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from SubscriptionApp.models import Subscriptions
from SubscriptionApp.serializers import SubscriptionSerializer

from django.core.files.storage import default_storage

from datetime import datetime
from twilio.rest import Client
import yfinance as yf
from yahoo_fin import stock_info as si

@csrf_exempt
def subscriptionApi(request,id=0):

    # Get all Subscriptions
    if request.method == 'GET':
        subscriptions = Subscriptions.objects.all()
        subscriptions_serializer = SubscriptionSerializer(subscriptions, many=True)
        return JsonResponse(subscriptions_serializer.data, safe=False)
        
    # Create Subscription
    elif request.method == 'POST':
        subscription_data=JSONParser().parse(request)

        subscription_data['SubscriptionStockTicker'] = subscription_data['SubscriptionStockTicker'].upper()
        subscription_data['SubscriptionStockTicker'] = ''.join(i for i in subscription_data['SubscriptionStockTicker'] if i.isalpha())
        subscription_data['SubscriptionContactNumber'] = ''.join(i for i in subscription_data['SubscriptionContactNumber'] if i.isdigit())

        # If Contact Number is not 10 length -> Error
        if len(subscription_data['SubscriptionContactNumber']) != 10:
            return JsonResponse("Error: Contact Number is Invalid", safe=False)

        # If Subscription already exists -> Error
        if Subscriptions.objects.filter(SubscriptionStockTicker=subscription_data['SubscriptionStockTicker'],SubscriptionContactNumber=subscription_data['SubscriptionContactNumber']).exists():
            return JsonResponse("Error: Dupicate Subscription", safe=False)

        # If Ticker isn't valid -> Error
        try:
            si.get_live_price(subscription_data['SubscriptionStockTicker'])
        except:
            print("An exception occurred")
            return JsonResponse("Error: Ticker "+subscription_data['SubscriptionStockTicker']+" does not exist", safe=False)

        # Validate Subscription inputs -> Save to Database
        subscription_serializer = SubscriptionSerializer(data=subscription_data)
        if subscription_serializer.is_valid():
            subscription_serializer.save()
            return JsonResponse("Added Successfully!!", safe=False)
        return JsonResponse("Failed to Add", safe=False)

    # Edit Subscription
    elif request.method=='PUT':
        subscription_data = JSONParser().parse(request)
        subscription = Subscriptions.objects.get(SubscriptionId=subscription_data['SubscriptionId'])
        subscriptions_serializer = SubscriptionSerializer(subscription,data=subscription_data)
        if subscriptions_serializer.is_valid():
            subscriptions_serializer.save()
            return JsonResponse("Updated Successfully!!", safe=False)
        return JsonResponse("Failed to Update.", safe=False)

    # Delete Subscription
    elif request.method =='DELETE':
        subscription = Subscriptions.objects.filter(SubscriptionId = id)
        subscription.delete()
        return JsonResponse("Deleted Successfully!!", safe=False)
        
# Manual Send Update API        
@csrf_exempt
def subscriptionSendUpdateApi(request,id=0):
    if request.method == 'POST':
        subscription_data=JSONParser().parse(request)
        subscription_serializer = SubscriptionSerializer(data=subscription_data)
        if subscription_serializer.is_valid():

            # Send SMS
            SendSms(subscription_data['SubscriptionContactNumber'],subscription_data['SubscriptionStockTicker']+": $"+str(round(si.get_live_price(subscription_data['SubscriptionStockTicker']), 2)))

            return JsonResponse("Sent Update Successfully!!", safe=False)
        return JsonResponse("Failed to Send Update", safe=False)

# Send Update to all Subscriptions
# This function is used by the Scheduler
def allSubscriptionsSendUpdate():

    # Get all Subscriptions
    subscriptions = Subscriptions.objects.all()

    # Parse unique Contact Numbers out of Subscriptions
    uniqueSubscriptions = subscriptions.values_list('SubscriptionContactNumber', flat=True).distinct()

    # Parse unique Stock Tickers out of Subscriptions
    uniqueTickers = subscriptions.values_list('SubscriptionStockTicker', flat=True).distinct()

    TickerPriceDictionary = dict()

    # Populate Ticker Price Dictionary with all required Stock Tickers
    for uniqueTicker in uniqueTickers:
        TickerPriceDictionary[uniqueTicker] = str(round(si.get_live_price(uniqueTicker), 2))

    # Combine all Stock Ticker prices into single SMS for each Contact Number
    for uniqueSubscription in uniqueSubscriptions:
        message = "Subscription Stock Prices:"
        subscriptionTickers = subscriptions.filter(SubscriptionContactNumber=uniqueSubscription).values_list('SubscriptionStockTicker', flat=True)
        for subscriptionTicker in subscriptionTickers:
            message += "\n"+subscriptionTicker + ": $"+ TickerPriceDictionary[subscriptionTicker]
        SendSms(uniqueSubscription,message)
    return

# Send SMS Twilio API Call
def SendSms(contact_number,message):
    account_sid = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    auth_token  = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    client = Client(account_sid, auth_token)
    try:
        message = client.messages.create(to="+1"+contact_number, from_="+XXXXXXXXXXX",body=message)
    except Exception:
        pass