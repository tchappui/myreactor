# Generated by Django 5.0.1 on 2024-01-26 12:16

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("players", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="player",
            options={"ordering": ("name",)},
        ),
        migrations.RemoveField(
            model_name="player",
            name="email",
        ),
        migrations.RemoveField(
            model_name="player",
            name="first_name",
        ),
    ]
