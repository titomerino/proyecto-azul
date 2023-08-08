from django.db import models
from django.utils.translation import gettext as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.files.base import ContentFile

from datetime import datetime

from project.models import Project, Zone
from entry.models import (
    PaymentService,
    PaymentOther,
)
from output.models import Output
from report.report_data import get_data_report

from utils.pdf import render_to_pdf


class Report(models.Model):
    """
    Guarda los reportes generados
    """
    OPTION_TYPE_CHOICES = [
        ('0', 'Reporte Mensual'),
        ('1', 'Ingresos por Zona'),
    ]

    title = models.CharField(_("Título"), max_length=150)
    project = models.ForeignKey(
        Project,
        related_name="reports",
        on_delete=models.CASCADE,
        verbose_name="Proyecto"
    )
    start_date = models.DateField(_("Desde"))
    end_date = models.DateField(_("Hasta"))
    report_pdf = models.FileField(_("Reporte"), upload_to='reports/')
    report_type = models.CharField(
        _("Tipo de report"),
        default='0',
        choices=OPTION_TYPE_CHOICES,
        max_length=2
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Reporte"
        verbose_name_plural = "Reportes"


@receiver(pre_save, sender=Report)
def pre_save_report_signal(sender, instance, *args, **kwargs):
    """
    Crea el report según los parametros del formulario
    asigna el nombre segúyn el título y fecha de creación
    """
    if instance.start_date and instance.end_date and instance.project:
        str_time = datetime.now().strftime("%m-%d-%Y--%H-%M-%S")
        title_pdf = instance.title.replace(' ', '-') + '--' + str_time + '.pdf'
        
        data = get_data_report(instance.project.id, instance)
        pdf = render_to_pdf('admin/reports.html', data)
        instance.report_pdf = ContentFile(pdf, name=title_pdf)
        # print(pdf)