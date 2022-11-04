# Generated by Django 3.2.15 on 2022-10-29 21:44

from django.db import migrations, models
import reports.models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0008_problemreported_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemreported',
            name='problem_id',
            field=models.CharField(blank=True, default=reports.models.random_id, max_length=12, unique=True),
        ),
    ]
