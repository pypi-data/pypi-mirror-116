# Generated by Django 3.2 on 2021-04-16 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UnitTestModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=20)),
                ("text", models.CharField(max_length=100)),
            ],
        ),
    ]
