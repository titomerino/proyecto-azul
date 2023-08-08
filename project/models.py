from django.db import models
from django.utils.translation import gettext as _


class Project(models.Model):
    """
    Contiene la información del proyecto
    de agua potable.
    """
    name = models.CharField(_("Nombre"), max_length=150, unique=True)
    description = models.TextField(_("Description"), blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"


class Zone(models.Model):
    """
    Representa la infoamción de las zonas que pertenecen a un proyecto.
    """
    project = models.ForeignKey(
        Project,
        related_name="zones",
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Proyecto"
    )
    name = models.CharField(_("Lugar"), max_length=250, unique=True)
    department = models.CharField(_("Departamento"), max_length=70)
    municipality = models.CharField(_("Municipio"), max_length=70)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Zona"
        verbose_name_plural = "Zonas"


class Rates(models.Model):
    """
    Representa los ragos de precios por metro cúbico de agua.
    """
    OPTION_PRICE_CHOICES = [
        ('0', 'metro'),
        ('1', 'cuota fija'),
    ]
    project = models.ForeignKey(
        Project,
        related_name="rates",
        on_delete=models.CASCADE,
        verbose_name="Proyecto"
    )
    title = models.CharField(_("Título"), max_length=150)
    min_meters = models.FloatField(_("Metros mínimos"), default=0)
    max_meters = models.FloatField(_("Metros máximos"), default=0)
    price = models.FloatField(_("Precio"), default=0)
    option_price = models.CharField(
        _("Precio por"),
        default='1',
        choices=OPTION_PRICE_CHOICES,
        max_length=2
    )
    state = models.BooleanField(_("Estado"), default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Tarifa"
        verbose_name_plural = "Tarifas"


class Member(models.Model):
    """
    Representa a los miembros o socios del proyecto. 
    """
    zone = models.ForeignKey(
        Zone,
        related_name="members",
        on_delete=models.CASCADE,
        verbose_name="Zona"
    )
    name = models.CharField(_("Nombre"), max_length=100)
    dui = models.CharField(_("DUI"), max_length=20)
    phone = models.CharField(_("Teléfono"), max_length=10)
    photo = models.ImageField(_("Foto"), blank=True, upload_to="members/photo")
    state = models.BooleanField(_("Estado"), default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Socio"
        verbose_name_plural = "Socios"


class Service(models.Model):
    """
    Representa la paja de agua o derecho
    """
    member = models.ForeignKey(
        Member,
        related_name="services",
        on_delete=models.CASCADE,
        verbose_name="Socio"
    )
    name = models.CharField(_("Nombre"), max_length=75)
    note = models.TextField(_("Nota"), blank=True)
    acquisition_date = models.DateField(_("Fecha de Adquisición"))
    price = models.FloatField(_("Precio de adquisición"))
    state = models.BooleanField(_("Activa"), default=True)
    paid = models.BooleanField(_("Pagada"), default=False)

    def __str__(self):
        return '{} -- ( {} )'.format(self.name, self.member.name)

    class Meta:
        verbose_name = "Paja"
        verbose_name_plural = "Pajas"
