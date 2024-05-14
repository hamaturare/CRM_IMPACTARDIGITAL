# Generated by Django 5.0.4 on 2024-05-14 13:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0027_rename_origin_lead_origin'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowUp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('planned_date', models.DateField(verbose_name='Data Prevista do Contato')),
                ('actual_date', models.DateField(blank=True, null=True, verbose_name='Data Realizada do Contato')),
                ('notes', models.TextField(blank=True, verbose_name='Anotações')),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leads.lead', verbose_name='Lead associada')),
            ],
        ),
    ]
