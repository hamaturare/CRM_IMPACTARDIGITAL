# Generated by Django 5.0.4 on 2024-06-17 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0014_remove_client_state_client_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
