# Generated by Django 3.2.18 on 2023-05-01 21:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
        ('output', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='output',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='outputs', to='project.project', verbose_name='Proyecto'),
        ),
    ]
