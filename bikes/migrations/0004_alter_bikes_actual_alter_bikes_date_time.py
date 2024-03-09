# Generated by Django 4.2.10 on 2024-03-09 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bikes", "0003_alter_bikes_date_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bikes",
            name="actual",
            field=models.DecimalField(decimal_places=1, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name="bikes", name="date_time", field=models.TextField(),
        ),
    ]