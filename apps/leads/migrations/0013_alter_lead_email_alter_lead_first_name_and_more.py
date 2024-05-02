# Generated by Django 5.0.4 on 2024-05-02 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0012_remove_lead_objective'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='email',
            field=models.EmailField(blank=True, max_length=255, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Nome da Lead'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Sobrenome da Lead'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='whatsapp',
            field=models.CharField(blank=True, max_length=20, verbose_name='Whatsapp (Telefone)'),
        ),
    ]
