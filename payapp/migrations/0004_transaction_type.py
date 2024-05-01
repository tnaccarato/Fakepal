# Generated by Django 5.0.2 on 2024-03-08 17:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('payapp', '0003_alter_account_currency_alter_request_receiver_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('request', 'Request'), ('transfer', 'Transfer')], default='transfer',
                                   max_length=10),
        ),
    ]
