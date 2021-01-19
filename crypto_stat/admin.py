from django.contrib import admin
from .models import Coin, Deal


@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost')


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('type', 'coin_name', 'count', 'coin_course', 'price', 'deal_time')
    readonly_fields = ('total',)
    list_filter = ('type', 'coin')

    def price(self, obj):
        return '%.2f $' % obj.total

    def deal_time(self, obj):
        return obj.date_time.strftime("%H:%M:%S %d/%m/%Y")

