from django.db import models
from django.conf import settings
from django.utils.timezone import now


class Coin(models.Model):
    class Meta:
        verbose_name = 'Coin'
        verbose_name_plural = 'Coins'

    name = models.CharField(unique=True, max_length=10)
    cost = models.FloatField()  # approximately in dollars

    @property
    def average_entry_point(self):
        total_spend = 0
        count_coin = 0
        for deal in self.coin_deal.all():
            if deal.type == "BUY":
                total_spend += deal.total
                count_coin += deal.count
            else:
                total_spend -= deal.count * (total_spend / count_coin)
                count_coin -= deal.count
        return total_spend / count_coin

    @property
    def total_bought(self):
        return self.coin_deal.filter(type="BUY").aggregate(sum=models.Sum('total'))

    @property
    def total_withdrawn(self):
        return self.coin_deal.filter(type="SELL").aggregate(sum=models.Sum('total'))

    def __str__(self):
        return f'{self.name} ~{self.cost}$'


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
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    coin_course = models.FloatField(default=0)
    count = models.FloatField()
    total = models.FloatField()
    date_time = models.DateTimeField(default=now, blank=True)

    @property
    def coin_name(self):
        return self.coin.name

    def save(self, *args, **kwargs):
        # TODO: sell deals save with minus
        # TODO: check if sell more then buy
        if self.coin_course > 0:
            self.total = self.count * self.coin_course
        else:
            self.total = self.count * self.coin.cost
            self.coin_course = self.coin.cost
        super().save(*args, **kwargs)

    def __str__(self):
        # TODO: change self.coin on actual coin name +actual course
        return f'{self.type} <b>{self.coin.name}</b> at the rate {self.coin_course}$ '
