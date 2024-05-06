# Generated by Django 5.0.4 on 2024-05-06 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_remove_client_first_contact_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='last_contact_date',
        ),
        migrations.AddField(
            model_name='client',
            name='next_contact_date',
            field=models.DateField(blank=True, null=True, verbose_name='Data próximo Contato'),
        ),
    ]
