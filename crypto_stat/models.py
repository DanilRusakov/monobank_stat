from django.db import models
from django.conf import settings
from django.utils.timezone import now


class Coin(models.Model):
    class Meta:
        verbose_name = 'Coin'
        verbose_name_plural = 'Coins'

    name = models.CharField(unique=True, max_length=10)
    cost = models.FloatField()  # approximately in dollars

    def __str__(self):
        return f'{self.name} ~{self.cost}$'


class CoinAveragePrice(models.Model):
    class Meta:
        verbose_name = 'Coin Average Price'
        verbose_name_plural = 'Coins Average Price'

    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name='coin_average_price')
    average_price = models.FloatField()
    spend_sum = models.FloatField(default=0.0)
    coin_profit = models.FloatField(default=0.0)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=now, blank=True)
    updated_at = models.DateTimeField(default=now, blank=True)
    # TODO: on save change only updated_at
    # TODO: fix added_by
    # TODO: add calculation spend sum



class Deal(models.Model):
    class Meta:
        verbose_name = 'Deal'
        verbose_name_plural = 'Deals'

    DEAL_TYPES = [
        ('BUY', 'buy'),
        ('SELL', 'sell'),
    ]

    type = models.CharField(choices=DEAL_TYPES, max_length=4, default='BUY')
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name='coin_deal')
    coin_course = models.FloatField(default=0)
    count = models.FloatField()
    total = models.FloatField()
    date_time = models.DateTimeField(default=now, blank=True)

    @property
    def coin_name(self):
        return self.coin.name

    def update_coin_average(self):
        coin_average = CoinAveragePrice.objects.filter(coin=self.coin)
        if coin_average.count():
            CoinAveragePrice.objects.update(average_price=self.coin_course)
        else:
            CoinAveragePrice.objects.create(coin=self.coin, average_price=self.coin_course)


    def save(self, *args, **kwargs):
        if self.coin_course > 0:
            self.total = self.count * self.coin_course
        else:
            self.total = self.count * self.coin.cost
            self.coin_course = self.coin.cost
        self.update_coin_average()
        super(Deal, self).save(*args, **kwargs)

    def __str__(self):
        # TODO: change self.coin on actual coin name +actual course
        return f'{self.type} {self.coin.name}'
