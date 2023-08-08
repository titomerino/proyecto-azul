from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.models import PaymentBase
from project.models import Project


class Output(PaymentBase):
    """
    Representa las salidas o egresos
    """
    project = models.ForeignKey(
        Project,
        related_name="outputs",
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Proyecto"
    )
    receiver_name = models.CharField(_("Nombre"), max_length=150)
    receiver_dui = models.CharField(_("DUI"), max_length=20)

    def __str__(self):
        return self.receiver_name
    
    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"