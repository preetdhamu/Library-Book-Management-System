# Generated by Django 4.1.7 on 2023-04-06 13:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_issuedbook_expiry_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issuedbook',
            old_name='subscriber_id',
            new_name='subscriber_username',
        ),
        migrations.AlterField(
            model_name='issuedbook',
            name='expiry_date',
            field=models.DateField(default=datetime.datetime(2023, 5, 6, 19, 18, 41, 448147)),
        ),
    ]
