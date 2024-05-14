# Generated by Django 5.0.4 on 2024-05-14 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0028_followup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followup',
            name='notes',
            field=models.TextField(blank=True, max_length=50, verbose_name='Anotações'),
        ),
        migrations.AlterField(
            model_name='followup',
            name='planned_date',
            field=models.DateField(verbose_name='Data do Próximo Contato'),
        ),
    ]
