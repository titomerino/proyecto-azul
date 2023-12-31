# Generated by Django 3.2.18 on 2023-04-12 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Título')),
                ('start_date', models.DateField(verbose_name='Desde')),
                ('end_date', models.DateField(verbose_name='Hasta')),
                ('report_pdf', models.FileField(upload_to='reports/', verbose_name='Reporte')),
                ('report_type', models.CharField(choices=[('0', 'Reporte Mensual'), ('1', 'Ingresos por Zona')], default='0', max_length=2, verbose_name='Tipo de report')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='project.project', verbose_name='Proyecto')),
            ],
            options={
                'verbose_name': 'Reporte',
                'verbose_name_plural': 'Reportes',
            },
        ),
    ]
