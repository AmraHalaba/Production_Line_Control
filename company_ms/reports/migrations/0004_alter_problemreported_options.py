# Generated by Django 3.2.15 on 2022-10-27 23:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_problemreported'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='problemreported',
            options={'verbose_name': 'problem reported', 'verbose_name_plural': 'problems reported'},
        ),
    ]
