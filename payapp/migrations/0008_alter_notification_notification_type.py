# Generated by Django 5.0.2 on 2024-03-17 16:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('payapp', '0007_notification_request_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('payment_sent', 'Payment Sent'), ('request_sent', 'Request Sent'),
                                            ('request_accepted', 'Request Accepted'),
                                            ('request_declined', 'Request Declined'),
                                            ('request_cancelled', 'Request Cancelled')], default='payment_sent',
                                   max_length=20),
        ),
    ]
