import json
from django.db.models import Sum, Count
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Cast
from django.db.models.fields import DateField, CharField
from .models import MonoPersonalStatement, MonoUser


class MonoView(LoginRequiredMixin, View):
    template_name = 'mono/spending_stat.html'

    def get(self, request):
        mono_user = MonoUser.objects.get(user=request.user)
        mono_statements = MonoPersonalStatement.objects.filter(mono_user=mono_user, hide_from_stat=False)
        spent_dates = mono_statements.filter(amount__lt=0)\
            .annotate(date_only=Cast('datetime', DateField())).values('date_only').order_by('date_only')\
            .annotate(total_sum=Sum('amount'), count=Count('amount'), total_cashback=Sum('cashback_amount'))
        spent_dates = list(map(lambda item: {
            'date': str(item['date_only']),
            'total_sum': item['total_sum'],
            'total_cashback': item['total_cashback']
        }, list(spent_dates)))
        biggest_spending = mono_statements.filter(amount__lt=0)\
            .order_by('description').values('description').annotate(total_sum=Sum('amount')).order_by('total_sum')[:10]

        balance = mono_statements.order_by('datetime').values('balance', 'datetime')
        balance = list(map(lambda item: {
            'date': str(item['datetime']),
            'balance': item['balance'],
        }, list(balance)))

        context = {
            'spent': json.dumps(spent_dates),
            'balance': json.dumps(balance),
            'transaction_count': mono_statements.count(),
            'income_transaction_count': mono_statements.filter(amount__gt=0).count(),
            'outcome_transaction_count': mono_statements.filter(amount__lt=0).count(),
            'biggest_spending': json.dumps(list(biggest_spending)),
        }
        return render(request, self.template_name, context)
