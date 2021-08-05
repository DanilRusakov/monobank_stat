from django.urls import path

from . import views

app_name = 'mono'
urlpatterns = [
    path('', views.MonoView.as_view(), name='index')
]
