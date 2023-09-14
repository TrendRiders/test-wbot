from django.urls import path
from twilio.rest import Client
from .views import bot

urlpatterns = [
    path('', bot),

]
