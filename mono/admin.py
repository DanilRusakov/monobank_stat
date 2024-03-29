from datetime import datetime
from django.contrib.admin import SimpleListFilter

from django.contrib import admin
from mono.models import MonoUser, MonoPersonalStatement


class MonoUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'mono_token')


class TransactionTypeFilter(SimpleListFilter):
    title = 'Type'
    parameter_name = 'type'

    def lookups(self, request, model_admin):
        return [('Income', 'Income'), ('Outcome', 'Outcome')]

    def queryset(self, request, queryset):
        if self.value() == 'Income':
            return queryset.filter(amount__gte=0)
        elif self.value() == 'Outcome':
            return queryset.filter(amount__lte=0)


class MonoPersonalStatementAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount_value', 'cashback_value', 'datetime')
    list_filter = (TransactionTypeFilter, )
    ordering = ['-datetime']
    admin_order_field = ('amount', 'cashback_amount', 'datetime')

    def cashback_value(self, obj):
        if obj.cashback_amount:
            return obj.cashback_amount/100
        else:
            return 0
    cashback_value.short_description = 'Cashback'
    cashback_value.admin_order_field = 'cashback_amount'

    def amount_value(self, obj):
        return obj.amount/100
    amount_value.short_description = 'Value'
    amount_value.admin_order_field = 'amount'


admin.site.register(MonoUser, MonoUserAdmin)
admin.site.register(MonoPersonalStatement, MonoPersonalStatementAdmin)
