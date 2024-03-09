# Generated by Django 4.2.11 on 2024-03-08 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("request", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="request", old_name="checkbox", new_name="checkbox1",
        ),
        migrations.AddField(
            model_name="request",
            name="checkbox2",
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="request",
            name="checkbox3",
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="request",
            name="textarea",
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
