# Generated by Django 5.0.4 on 2024-05-03 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0013_alter_lead_email_alter_lead_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='return_contac',
            field=models.DateField(blank=True, null=True, verbose_name='Retornar Contato Em'),
        ),
    ]
