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
    def total_count(self):
        total_spend = 0
        count_coin = 0
        for deal in self.coin_deal.all():
            if deal.type == "BUY":
                total_spend += deal.total
                count_coin += deal.count
            else:
                total_spend -= deal.total
                count_coin -= deal.count
        return total_spend/count_coin

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
        coin_average_record = CoinAveragePrice.objects.filter(coin=self.coin)
        new_coin_average = self.calculate_coin_average_by_deals()
        if coin_average_record.count():
            coin_average_record.update(average_price=self.coin_course)
        else:
            CoinAveragePrice.objects.create(coin=self.coin, average_price=self.coin_course)

    def calculate_coin_average_by_deals(self):
        all_coin_deals = Deal.objects.filter(coin=self.coin)
        spend_sum = 0
        buy_coin_count = 0
        sell_coin_count = 0
        withdrawn_sum = 0
        for deal in all_coin_deals:
            if deal.type == 'BUY':
                spend_sum += deal.total
                buy_coin_count += deal.count
            else:
                withdrawn_sum -= deal.total
                sell_coin_count += deal.count
        # current_count=buy_coin_count-sell_coin_count
        average_price = spend_sum-withdrawn_sum
        result = {
            'spend_sum': spend_sum,
            # 'current_count': current_count,
            'average_price': 0,
            'withdrawn_sum': withdrawn_sum
        }

        return result

    def save(self, *args, **kwargs):
        # TODO: sell deals save with minus
        # TODO: check if sell more then buy
        if self.coin_course > 0:
            self.total = self.count * self.coin_course
        else:
            self.total = self.count * self.coin.cost
            self.coin_course = self.coin.cost
        self.update_coin_average()
        super().save(*args, **kwargs)

    def __str__(self):
        # TODO: change self.coin on actual coin name +actual course
        return f'{self.type} <b>{self.coin.name}</b> at the rate {self.coin_course}$ '
