# Generated by Django 5.0.1 on 2024-01-26 12:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("casestudy", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="casestudy",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
