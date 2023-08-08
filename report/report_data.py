from project.models import (
    Project,
    Zone,
    Service,
)
from entry.models import (
    PaymentOther,
    PaymentService,
    MonthlyFee,
)
from output.models import Output
from datetime import datetime


# Suma todos los ingresos por cuotas mensuales
# agrupados por zona
def get_total_monthly_fee_by_zone(zone_id, from_date, until_date):
    """
    Obtiene el total de los ingresos por servicio de agua
    según zona
    """
    payments = MonthlyFee.objects.filter(
        service__member__zone=zone_id,
        payment_date__range = [from_date, until_date],
        state=True
    )
    total = 0
    for payment in payments:
        total += payment.amount
    return total

def get_total_payment_other(zone_id):
    """
    Obtiene el total de los ingresos por otros ingresos 
    según la zona
    """
    return ''

# Crea el bloque de ingresos por zona
def get_zone_report(project_id, from_date, until_date):
    """
    Lista las zonas y crea un objeto zona donde va el total
    de ingresos.
    """
    zones_instances = Zone.objects.filter(project=project_id)

    zones_data = []
    zones_total = 0
    for zone in zones_instances:
        calculation = get_total_monthly_fee_by_zone(zone.id, from_date, until_date)
        zones_total += calculation
        zones_data.append(
            {
                "name": zone.name,
                "total": calculation
            }
        )
    return {
        "zones_data": zones_data,
        "total": zones_total
    }


def get_total_payment_service_by_type(zone_id, type):
    """
    Obtiene el total de ingreso por tipo
    """
    pass

def get_total_payment_service(project_id, from_date, until_date):
    payments = PaymentService.objects.filter(
        service__member__zone__project=project_id,
        register_date__range = [from_date, until_date]
    )
    total = 0
    for payment in payments:
        total += payment.amount
    return total

def get_all_outputs(project_id, from_date, until_date):
    """
    Obtiene todos los egresos
    """
    outpust = Output.objects.filter(
        project = project_id, register_date__range = [from_date, until_date]
    )
    data = []
    for item in outpust:
        data.append(
            {
                'title': item.note,
                'amount': item.amount
            }
        )

    return data


def get_data_report(project_id, instance):
    project_instance = Project.objects.get(id=project_id)
    zones_data = []
    zones_entry = get_zone_report(project_id, instance.start_date, instance.end_date)
    other_entry = get_total_payment_service(project_id, instance.start_date, instance.end_date)
    data = {
        "project": {
            "name": project_instance.name,
        },
        "report": {
            "start_date": instance.start_date.strftime("%m de %B %Y"),
            "end_date": instance.end_date.strftime("%m de %B %Y"),
        },
        "entries": {
            "zones": {
                "title": "Cobro por servicio de agua:",
                "entries": zones_entry,
            },
            "others": {
                "title": "Aperturas, abonos y cancelaciones de ventas de acometidas domiciliares",
                "total": other_entry,
            },
            "total": zones_entry['total'] + other_entry    
        },
        "outputs": get_all_outputs(project_id, instance.start_date, instance.end_date)
    }
    print(data)
    return data