from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import Coin, Deal


class CoinView(View):
    template_name = 'crypto/coins_list.html'

    def get(self, request):
        coins = Coin.objects.all()
        deals = Deal.objects.all()
        context = {
            'coins': coins,
            'deals': deals,
        }
        return render(request, self.template_name, context)
