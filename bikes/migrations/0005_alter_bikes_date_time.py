# Generated by Django 4.2.10 on 2024-03-11 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bikes", "0004_alter_bikes_actual_alter_bikes_date_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bikes", name="date_time", field=models.TextField(unique=True),
        ),
    ]
