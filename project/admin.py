from django.contrib import admin
from django.utils.translation import ugettext_lazy
from django.utils.translation import gettext_lazy as _
from django import forms

from import_export import resources
from import_export.admin import ExportActionModelAdmin

from .models import (
    Project,
    Zone,
    Rates,
    Member,
    Service,
)
from entry.models import ServiceProxy

#-------- Admin site --------
admin.site.index_title = "ACASA Posa Azul"
admin.site.site_header = "ACASA Administración"
admin.site.site_title = "ACASA Posa Azul"
# ---------------------------


# Import Export classes
class MemberResource(resources.ModelResource):
    """
    Exporta he importa toda la data de socios
    """

    class Meta:
        model = Member


class ServiceResource(resources.ModelResource):
    """
    Exporta he importa pajas de agua
    """
    class Meta:
        model = Service


class RatesResource(resources.ModelResource):
    """
    Exporta he importa tarifas
    """
    class Meta:
        model = Rates


class ZoneResource(resources.ModelResource):
    """
    Exporta he importa cobros
    """
    fields = (
        'name',
        'department',
        'municipality',
        'project__name',
    )

    class Meta:
        model = Zone
# --------------------------


# ------ Project --------
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_per_page = 10
# Project end


# ------- Zone --------
@admin.register(Zone)
class ZoneAdmin(ExportActionModelAdmin):
    search_fields = ('name',)
    list_filter = ('project__name', 'department', 'municipality')
    list_display = ('name', 'department', 'municipality', 'project')
    list_per_page = 10
# Zone end


# -------- Rates --------
@admin.register(Rates)
class RatesAdmin(ExportActionModelAdmin):
    list_display = ('title',
        'min_meters',
        'max_meters',
        'price',
        'option_price',
        'state',
        'project',
    )
    list_filter = ('project__name',)
    list_per_page = 10
# Rates end


# ------- Members --------
class ServiceInline(admin.StackedInline):
    model = Service
    classes = ['collapse']
    fields = (
        'name',
        ('acquisition_date', 'price'),
        'note',
        'paid',
        'state',
    )
    extra = 0


@admin.register(Member)    
class MemberAdmin(ExportActionModelAdmin):
    inlines = [ServiceInline]
    fieldsets = (
        ('Información Personal', {
            'fields': (
                'name',
                ('dui', 'phone'),
                ('zone', 'photo'),
                'state'
            )
        }),
    )
    list_display = ('name', 'dui', 'phone', 'zone', 'state')
    list_filter = (
        'zone__project__name',
        'zone__department',
        'zone__municipality',
        'zone__name',
    )
    search_fields = ('name', 'dui', 'phone')
    list_per_page = 10
# members end


# -------- Services ---------
class ServiceForm(forms.ModelForm):
    """
    Desactiva el campo "price" si ya hay cobros asignados a 
    la paja de agua, para que este no pueda ser modificado.
    """
    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        if self.instance.id != None:
            total_payment = ServiceProxy.objects.get(id=self.instance.id).total_payment()
            if total_payment > 0:
                # self.fields['price'].widget.attrs['readonly'] = True
                self.fields['price'].disabled = True
                self.fields['price'].help_text = 'El precio no puede ser modificado por que ya existen cobros asociados'

    class Meta:
        model = Service
        exclude = ('',) 


@admin.register(Service)
class ServiceAdmin(ExportActionModelAdmin):
    form = ServiceForm
    list_select_related = ('member',)
    autocomplete_fields  = ('member',)
    fields = (
        'member',
        'name',
        ('acquisition_date', 'price'),
        'note',
        'paid',
        'state',
    )
    list_display = (
        'name',
        'member',
        'acquisition_date',
        'price',
        'paid',
        'state',
    )
    readonly_fields = ('paid',)
    list_filter = (
        'member__zone__department',
        'member__zone__municipality',
        'member__zone__name',
        'paid',
    )
    search_fields = ('name', 'member__name')
    raw_id_fields = ('member',)
    list_per_page = 10
# services end