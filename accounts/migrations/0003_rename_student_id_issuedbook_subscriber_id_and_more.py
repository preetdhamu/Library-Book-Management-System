# Generated by Django 4.1.7 on 2023-04-05 01:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_book_issuedbook'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issuedbook',
            old_name='student_id',
            new_name='subscriber_id',
        ),
        migrations.AlterField(
            model_name='issuedbook',
            name='expiry_date',
            field=models.DateField(default=datetime.datetime(2023, 4, 19, 6, 41, 46, 451160)),
        ),
    ]
