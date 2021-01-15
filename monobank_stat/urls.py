from django.contrib import admin
from django.urls import path, include
from info import views as info_views

urlpatterns = [
    path('', info_views.IndexView.as_view()),
    path('admin/', admin.site.urls),
    path('coins/', include('crypto_stat.urls'))
]
