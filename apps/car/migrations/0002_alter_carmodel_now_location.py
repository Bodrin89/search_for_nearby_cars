# Generated by Django 5.0.3 on 2024-03-26 13:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0001_initial'),
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carmodel',
            name='now_location',
            field=models.ForeignKey(default=14529, on_delete=django.db.models.deletion.PROTECT, related_name='now_location', to='location.locationmodel', verbose_name='Текущая локация'),
        ),
    ]