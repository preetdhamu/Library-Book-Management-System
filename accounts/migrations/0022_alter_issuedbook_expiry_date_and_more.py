# Generated by Django 4.1.7 on 2023-05-01 12:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_book_status_alter_issuedbook_expiry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issuedbook',
            name='expiry_date',
            field=models.DateField(default=datetime.datetime(2023, 5, 31, 17, 31, 22, 712195)),
        ),
        migrations.AlterField(
            model_name='issuedbook',
            name='subscriber_username',
            field=models.CharField(max_length=100),
        ),
    ]
