from django.contrib import admin
from django.urls import path, include
from info import views as info_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', info_views.IndexView.as_view(), name="home"),
    # Login and Logout
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    path('admin/', admin.site.urls),
    path('coins/', include('crypto_stat.urls')),
    path('oauth/', include('social_django.urls', namespace='social'))
]
