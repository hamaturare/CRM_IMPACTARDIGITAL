# Generated by Django 5.0.4 on 2024-05-13 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_alter_client_client_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='client_info',
            field=models.TextField(blank=True, max_length=2500, verbose_name='Informações Sobre a Lead'),
        ),
    ]