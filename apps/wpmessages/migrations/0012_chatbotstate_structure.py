# Generated by Django 5.0.4 on 2024-06-10 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wpmessages', '0011_remove_chatbotstate_structure'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatbotstate',
            name='structure',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
