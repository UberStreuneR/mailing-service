# Generated by Django 4.0.4 on 2022-05-25 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_message_mailing_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailing',
            name='clients',
        ),
        migrations.RemoveField(
            model_name='mailing',
            name='filter',
        ),
        migrations.AddField(
            model_name='mailing',
            name='filter_operator_code',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='mailing',
            name='fitler_tag',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]