from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('chat_screen/',views.chatbot, name='chat_screen'), 
    path('getResponse/',views.get_response, name='get_response')   
]