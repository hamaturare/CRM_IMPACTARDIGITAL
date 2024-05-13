# Generated by Django 5.0.4 on 2024-05-06 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0017_alter_servicetype_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='last_name',
        ),
        migrations.AddField(
            model_name='lead',
            name='company_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Empresa da Lead'),
        ),
    ]