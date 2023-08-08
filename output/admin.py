from django.contrib import admin

from daterange.filters import DateRangeFilter
from import_export import resources
from import_export.fields import Field
from import_export.admin import ExportActionModelAdmin

from output.models import Output


class OutputResource(resources.ModelResource):
    """
    Exporta he import pagos o salidas
    """
    # Cambiamos los nombres de las columnas del archivo donde se
    # exporta
    name = Field(attribute='receiver_name', column_name='Nombre')
    dui = Field(attribute='receiver_dui', column_name='DUI')
    date = Field(attribute='register_date', column_name='Fecha de registro')
    number = Field(attribute='receipt_number', column_name='N° de recibo')
    amount = Field(attribute='amount', column_name='Total pagado')
    note = Field(attribute='note', column_name='A concepto de')
    
    class Meta:
        model = Output
        fields = (
            'name',
            'dui',
            'date',
            'number',
            'amount',
            'note',
        )
        exclude = ('id',)


@admin.register(Output)
class OutputAdmin(ExportActionModelAdmin):
    resource_class = OutputResource
    fields = (
        'project',
        ('receiver_name', 'receiver_dui'),
        ('register_date', 'receipt_number'),
        'amount',
        'note',
    )
    list_display = (
        'receiver_name',
        'receiver_dui',
        'amount',
        'receipt_number',
        'register_date',
    )
    search_fields = (
        'receiver_name',
        'receiver_dui',
        'receipt_number',
    )
    list_filter = [
        ('register_date', DateRangeFilter),
    ]
    change_list_template = "admin/daterange/change_list.html"

