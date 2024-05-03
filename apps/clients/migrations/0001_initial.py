# Generated by Django 5.0.4 on 2024-05-03 16:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome do Objetivo')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Dia que a Lead Chegou')),
                ('first_contact_date', models.DateField(blank=True, null=True, verbose_name='Data Primeiro Contato')),
                ('company_name', models.CharField(blank=True, max_length=255, verbose_name='Nome da Lead')),
                ('client_name', models.CharField(blank=True, max_length=255, verbose_name='Nome da Lead')),
                ('email', models.EmailField(blank=True, max_length=255, verbose_name='Email')),
                ('instagram', models.CharField(blank=True, max_length=50, null=True, verbose_name='Instagram')),
                ('website', models.URLField(blank=True, null=True, verbose_name='Website')),
                ('whatsapp', models.CharField(blank=True, max_length=20, verbose_name='Whatsapp (Telefone)')),
                ('priority', models.IntegerField(verbose_name='Prioridade')),
                ('city', models.CharField(blank=True, max_length=50, verbose_name='Cidade')),
                ('state', models.CharField(blank=True, max_length=2, verbose_name='Estado')),
                ('client_kpis', models.IntegerField(verbose_name='KPIs')),
                ('client_income', models.IntegerField(verbose_name='Receita Mensal')),
                ('client_budget', models.IntegerField(verbose_name='Gasto Máximo Mensal')),
                ('service_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clients.servicetype', verbose_name='Tipos de Serviço da Lead')),
            ],
        ),
    ]
