from django.db import models
from django.utils.timezone import now


class Client(models.Model):

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    client_id = models.CharField(max_length=15, blank=True)
    name = models.CharField(max_length=50, blank=True)
    mono_token = models.CharField(max_length=50, unique=True)
    date_time = models.DateTimeField(default=now, blank=True)

    # def save(self, force_insert=False, force_update=False, *args, **kwargs):
    #     if self.mono_token:
    #         print(self.mono_token)
    #         return False
    #
    #     super(Client, self).save(force_insert, force_update, *args, **kwargs)
    #     self.__original_name = self.name


class ClientAccounts(models.Model):

    class Meta:
        verbose_name = 'Client Account'

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    account_id = models.CharField(max_length=22, unique=True)
    currency_code = models.IntegerField()
    balance = models.IntegerField(default=0)
    credit_limit = models.IntegerField(default=0)
