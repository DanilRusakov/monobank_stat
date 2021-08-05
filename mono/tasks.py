from datetime import datetime, timedelta

from celery import shared_task
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import MonoUser, MonoPersonalStatement
import requests


@shared_task
def parse_statements():
     timedelta_from = (datetime.today().replace(microsecond=0) - timedelta(days=31)).timestamp()
     user = User.objects.first()
     mono_user = get_object_or_404(MonoUser, user=user)
     url = 'https://api.monobank.ua/personal/statement/0/' + str(int(timedelta_from)) + '/'
     r = requests.get(url, headers={'X-Token': mono_user.mono_token})
     if r.status_code == 200:
          data = r.json()
          for row in data:
               MonoPersonalStatement.objects.update_or_create(
                    transaction_id=row['id'],
                    mono_user=mono_user,
                    defaults={
                         'time': row['time'],
                         'datetime': datetime.fromtimestamp(row['time']),
                         'description': row['description'],
                         'amount': row['amount'],
                         'operation_amount': row['operationAmount'],
                         'currency_code': row['currencyCode'],
                         'commission_rate': row['commissionRate'],
                         'cashback_amount': row['cashbackAmount'],
                         'balance': row['balance'],
                         'receipt_id': row.get('receiptId', '')
                    }
               )
     else:
          print(r.json()['errorDescription'])
