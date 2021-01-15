from django.urls import path

from . import views

app_name = 'crypto'
urlpatterns = [
    path('', views.CoinView.as_view(), name='index')
]
