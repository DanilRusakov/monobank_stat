from django.contrib import admin
from .models import Coin, Deal


@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost')


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('type', 'coin_name', 'count', 'coin_course', 'price', 'deal_time')
    readonly_fields = ('total',)

    def price(self, obj):
        return f'{obj.total}$'

    def deal_time(self, obj):
        return obj.date_time.strftime("%H:%M:%S %d/%m/%Y")

