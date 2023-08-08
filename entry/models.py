from django.db import models
from django.utils.translation import gettext as _
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from project.models import Service, Rates

from utils.models import PaymentBase


class PaymentOther(PaymentBase):
    """
    Rrepesenta a los ingresos por otras fuentes.
    """
    def __str__(self):
        return str(self.register_date)

    class Meta:
        verbose_name = 'Otro ingreso'
        verbose_name_plural = 'Otros ingresos'


class PaymentService(PaymentBase):
    """
    Representa el ingreso por cuota, cuando no se hace un 
    solo pago por una paja de agua.
    """
    OPTION_TYPE_CHOICES = [
        ('0', 'Cuota por paja'),
        ('1', 'Cobro por activación'),
    ]
    service = models.ForeignKey(
        Service,
        related_name = "payments",
        on_delete = models.CASCADE,
        verbose_name = "Paja de agua"
    )
    payment_type = models.CharField(
        _("Tipo de cobro"),
        default='0',
        choices=OPTION_TYPE_CHOICES,
        max_length=2
    )

    def __str__(self):
        return str(self.register_date)

    def clean(self):
        try:
            self.service
        except Exception as e:
            return e

        # Evalúa que los cobros no supere el precio de la paja de agua.
        service_proxy = ServiceProxy.objects.get(id=self.service.id)
        total_payment = service_proxy.total_payment()
        # Aplica cuando es un cobro nuevo
        if self.payment_type == '0':
            if self.id == None:
                if (total_payment + self.amount) > self.service.price:
                    raise ValidationError({
                        'amount': _('Actualmente solo debes ${}'.format(self.service.price - total_payment))
                    })
            # Aplica cuando es una actualización de un cobro
            else:
                old_instance = PaymentService.objects.get(id=self.id)
                total_less_old_amount = total_payment - old_instance.amount
                if (total_less_old_amount + self.amount) > self.service.price:
                    raise ValidationError({
                        'amount': _('Actualmente solo debes ${}'.format(self.service.price - total_less_old_amount))
                    })


    class Meta:
        verbose_name = "Cobro"
        verbose_name_plural = "Cobros"

@receiver(post_save, sender=PaymentService)
def post_save_payment_service_signal(sender, instance, created, **kwargs):
    # Disparador que actualiza el estado de la paja de agua
    # si ya fue pagada completamente, solo si es de tipo "cobro por paja"
    if instance.payment_type == '0':
        service_proxy = ServiceProxy.objects.get(id=instance.service.id)
        total_payment = service_proxy.total_payment()
        if instance.service.price == total_payment:
            instance.service.paid = True
            instance.service.save()

    
# Añade una función al modelo de Service que calcula el total pagado
# del derecho de agua.
class ServiceProxy(Service):
    """
    Añadimos un proxy al modelo Service para poder calcular 
    el total pagado de la paja de agua.
    """
    class Meta:
        proxy = True

    def total_payment(self):
        total = 0
        payments = PaymentService.objects.filter(service_id=self.id, payment_type='0')
        for item in payments:
            print(item.payment_type)
            total = total + item.amount
        return total



class MonthlyFee(models.Model):
    """
    Representa los ingresos mensuales por cobro a paja
     de agua.
    """
    service = models.ForeignKey(
        Service,
        related_name="monthly_fee",
        on_delete=models.CASCADE,
        verbose_name="Paja de agua"
    )
    note = models.TextField(_("Nota"), blank=True)
    payment_date = models.DateField(_("Fecha de lectura"))
    previous_meters = models.FloatField(
        _("Lectura anterior"),
        help_text="Corresponde a la lectura del mes anterior"
    )
    current_meters = models.FloatField(_("Lectura actual"))
    receipt_number = models.CharField(_("N° de recibo"), max_length=25)
    state = models.BooleanField(_("Pagado"), default=False)
    meters = models.FloatField(_("Metros consumidos"))
    amount = models.FloatField(_("Total a pagar"))

    def __str__(self):
        return str(self.payment_date)

    def clean(self):
        try:
            self.service
        except Exception as e:
            return e
        
        if not self.service.state:
            raise ValidationError({
                'service': _('La paja de agua se encuentra inactiva')
            })
        if self.previous_meters and self.current_meters and self.previous_meters > self.current_meters:
            raise ValidationError({
                'current_meters': _('La lectura actual no puede ser menor a la anterior')
            })
    
    class Meta:
        verbose_name = "Cuota"
        verbose_name_plural = "Cuotas"


# Payments Signals
def calculate_amount_meters(meters):
    """
    Calculará los metros consumidos y el costo del cobro.
    """
    rates = Rates.objects.filter(state=True)

    for rate in rates:
        if meters >= rate.min_meters and meters < rate.max_meters:
            if rate.option_price == '1':
                return rate.price
            else:
                return rate.price * meters
            break
    return 0

@receiver(pre_save, sender=MonthlyFee)
def pre_save_payment_signal(sender, instance, **kwargs):
    """
    Se detona justo antes de guardar o actualizar un pago.
    """
    instance.meters = instance.current_meters - instance.previous_meters
    instance.amount = calculate_amount_meters(instance.meters)
