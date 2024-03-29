from django.db import models
from django.contrib.auth.models import User


class MonoUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mono_token = models.CharField(max_length=50, blank=True)
    # is_parsed = models.BooleanField(default=False)


class MonoPersonalStatement(models.Model):
    mono_user = models.ForeignKey(MonoUser, on_delete=models.CASCADE)
    transaction_id = models.CharField(verbose_name='Transaction id', max_length=16, unique=True)
    time = models.PositiveIntegerField()
    datetime = models.DateTimeField()
    description = models.CharField(max_length=255, blank=True)
    amount = models.IntegerField()
    operation_amount = models.IntegerField()
    currency_code = models.IntegerField()
    commission_rate = models.IntegerField()
    cashback_amount = models.IntegerField()
    balance = models.IntegerField()
    receipt_id = models.CharField(max_length=19, blank=True)
    hide_from_stat = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Transaction'

    def __str__(self):
        if self.description:
            return self.description
    # TODO: add property for displaying and filtering in admin panel