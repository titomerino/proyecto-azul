from django.db import models
from django.utils.translation import gettext as _
from datetime import date


class PaymentBase(models.Model):
    """
    Modelo abstracto para ingresos
    Defeine los campos comunes
    """
    register_date = models.DateField(
        _("Fecha de registro"),
        default = date.today
    )
    note = models.TextField(_("Nota"), blank=True)
    receipt_number = models.CharField(_("N° de recibo"), max_length=25)
    amount = models.FloatField(_("Total a pagar"))

    class Meta:
        abstract = True
