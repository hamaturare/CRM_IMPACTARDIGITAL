# Generated by Django 5.0.4 on 2024-06-04 01:12

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wpmessages', '0002_alter_wpmessage_business_phone_number_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wpmessage',
            old_name='timestamp',
            new_name='message_timestamp',
        ),
        migrations.AddField(
            model_name='wpmessage',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='wpmessage',
            name='lead_phone_number',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
