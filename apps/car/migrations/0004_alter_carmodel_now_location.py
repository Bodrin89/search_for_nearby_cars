# Generated by Django 5.0.3 on 2024-03-26 13:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0003_alter_carmodel_now_location'),
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carmodel',
            name='now_location',
            field=models.ForeignKey(default=25734, on_delete=django.db.models.deletion.PROTECT, related_name='now_location', to='location.locationmodel', verbose_name='Текущая локация'),
        ),
    ]
