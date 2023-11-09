# Generated by Django 4.2.7 on 2023-11-03 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Doctor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
                ("hospital", models.CharField(max_length=50)),
                ("department", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Patient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="Opening_hour",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("day", models.IntegerField()),
                ("work", models.BooleanField()),
                ("lunch", models.BooleanField()),
                ("start", models.CharField(max_length=4)),
                ("end", models.CharField(max_length=4)),
                ("lunch_start", models.CharField(max_length=4)),
                ("lunch_end", models.CharField(max_length=4)),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="opentimes",
                        to="accounts.doctor",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="No_covered",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("subject", models.CharField(max_length=100)),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="nocovers",
                        to="accounts.doctor",
                    ),
                ),
            ],
        ),
    ]
