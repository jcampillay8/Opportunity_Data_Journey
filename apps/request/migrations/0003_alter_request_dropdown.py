# Generated by Django 4.2.11 on 2024-03-10 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "request",
            "0002_rename_checkbox_request_checkbox1_request_checkbox2_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="request",
            name="dropdown",
            field=models.CharField(
                choices=[("option1", "Opción 1"), ("option2", "Opción 2")],
                max_length=200,
            ),
        ),
    ]
