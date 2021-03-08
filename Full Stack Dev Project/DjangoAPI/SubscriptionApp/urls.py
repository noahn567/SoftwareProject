from django.conf.urls import url
from SubscriptionApp import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    url(r'^subscription/$',views.subscriptionApi),
    url(r'^subscription/([0-9]+)$',views.subscriptionApi),

    url(r'^subscription/sendupdate$',views.subscriptionSendUpdateApi)
]