from django.contrib import admin
from django.urls import path, include
from . import views
from .forms import LoginForm
from django.contrib.auth.views import LoginView,LogoutView

app_name = 'accounts'

urlpatterns = [
    path('signup/',views.signup, name='signup'),
    path('login/',LoginView.as_view(template_name = 'accounts/login.html', form_class = LoginForm), name='login'),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('upload/', views.upload_file, name='upload_file'),
    path('dashboard/', views.dashboard, name='dashboard'),   
]


