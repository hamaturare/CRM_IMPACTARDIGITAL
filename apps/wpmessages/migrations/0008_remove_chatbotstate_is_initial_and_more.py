# Generated by Django 5.0.4 on 2024-06-09 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wpmessages', '0007_chatbotquestion_custom_field_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatbotstate',
            name='is_initial',
        ),
        migrations.RemoveField(
            model_name='wpmessage',
            name='custom_data',
        ),
        migrations.AlterField(
            model_name='chatbotquestion',
            name='custom_field_name',
            field=models.CharField(max_length=100),
        ),
    ]
