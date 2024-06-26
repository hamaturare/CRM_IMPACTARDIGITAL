# Generated by Django 5.0.4 on 2024-05-06 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_client_client_info'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='first_contact_date',
        ),
        migrations.AddField(
            model_name='client',
            name='contract_date',
            field=models.DateField(blank=True, null=True, verbose_name='Data do Contrato'),
        ),
        migrations.AddField(
            model_name='client',
            name='last_contact_date',
            field=models.DateField(blank=True, null=True, verbose_name='Data do Contrato'),
        ),
        migrations.AlterField(
            model_name='client',
            name='client_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Nome do Cliente'),
        ),
        migrations.AlterField(
            model_name='client',
            name='company_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Nome da Empresa'),
        ),
        migrations.AlterField(
            model_name='servicetype',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Serviço Prestado'),
        ),
    ]
