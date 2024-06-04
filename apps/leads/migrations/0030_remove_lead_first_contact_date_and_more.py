# Generated by Django 5.0.4 on 2024-06-04 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0029_alter_followup_notes_alter_followup_planned_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='first_contact_date',
        ),
        migrations.AddField(
            model_name='lead',
            name='last_contact_date',
            field=models.DateField(blank=True, null=True, verbose_name='Data do Último Contato'),
        ),
        migrations.AlterField(
            model_name='followup',
            name='actual_date',
            field=models.DateField(blank=True, null=True, verbose_name='Data do Último Contato'),
        ),
    ]
