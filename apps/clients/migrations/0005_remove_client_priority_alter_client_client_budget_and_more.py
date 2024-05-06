# Generated by Django 5.0.4 on 2024-05-06 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_remove_client_last_contact_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='priority',
        ),
        migrations.AlterField(
            model_name='client',
            name='client_budget',
            field=models.CharField(blank=True, max_length=50, verbose_name='Gasto Máximo Mensal'),
        ),
        migrations.AlterField(
            model_name='client',
            name='client_income',
            field=models.CharField(blank=True, max_length=50, verbose_name='Valor do Contrato'),
        ),
        migrations.AlterField(
            model_name='client',
            name='client_kpis',
            field=models.CharField(blank=True, max_length=50, verbose_name='KPIs'),
        ),
    ]
