from django.contrib import admin

from daterange.filters import DateRangeFilter
from import_export import resources
from import_export.admin import ExportActionModelAdmin

from .models import (
    PaymentService,
    PaymentOther,
    MonthlyFee,
)


# ------ Impoert Export Models
class MonthlyFeeResource(resources.ModelResource):
    """
    Exporta he importa cobros
    """
    class Meta:
        model = MonthlyFee


class PaymentOtherResource(resources.ModelResource):
    """
    Exporta he importa otros cobros.
    """
    class Meta:
        model = PaymentOther


class PaymentServiceResource(resources.ModelResource):
    """
    Exporta he importa pagos de pajas de agua
    """
    class Meta:
        model = PaymentService
# --------------------------


# ------- Payments ---------
@admin.register(MonthlyFee)
class MonthlyFeeAdmin(ExportActionModelAdmin):
    list_select_related = ('service',)
    autocomplete_fields  = ('service',)
    fields = (
        'service',
        ('receipt_number', 'payment_date'),
        ('previous_meters', 'current_meters'),
        ('meters', 'amount'),
        'note',
        'state',
    )
    list_display = (
        'service',
        'meters',
        'amount',
        'payment_date',
        'note',
        'state',
    )
    readonly_fields = ('meters', 'amount')
    list_filter = [
        ('payment_date', DateRangeFilter),
        'state',
        'service__member__zone__name',
    ]
    search_fields = ('payment_date', 'service__member__name')
    raw_id_fields = ('service',)
    list_per_page = 10
    change_list_template = "admin/daterange/change_list.html"
# payments end


# -------- Entry ---------
@admin.register(PaymentService)
class PaymentServiceAdmin(ExportActionModelAdmin):
    list_select_related = ('service',)
    autocomplete_fields  = ('service',)
    fields = (
        ('service', 'payment_type'),
        ('receipt_number', 'register_date'),
        'amount',
        'note',
        # 'state',
    )
    list_display = (
        'service',
        'amount',
        'register_date',
        'payment_type',
        # 'state',
    )
    list_filter = [
        ('register_date', DateRangeFilter),
        # 'state',
        'service__member__zone__name',
    ]
    search_fields = ('service__member__name',)
    raw_id_fields = ('service',)
    list_per_page = 10
    change_list_template = "admin/daterange/change_list.html"
# ------------------------


# -------- Payment Other ---------
@admin.register(PaymentOther)
class PaymentOtherAdmin(ExportActionModelAdmin):
    list_display = (
        'register_date',
        'receipt_number',
        'amount',
        'note',
    )
    fields = (
        ('receipt_number', 'register_date'),
        'amount',
        'note',
    )
    list_filter = [
        ('register_date', DateRangeFilter),
    ]
    list_per_page = 10
    change_list_template = "admin/daterange/change_list.html"
# --------------------------------