# Generated by Django 3.1.4 on 2020-12-28 18:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("jet", "0003_auto_20201228_1540"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bookmark",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="user",
            ),
        ),
    ]
