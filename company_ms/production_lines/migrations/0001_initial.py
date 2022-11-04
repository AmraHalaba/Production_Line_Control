# Generated by Django 3.2.15 on 2022-10-27 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0002_auto_20221027_1947'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductionLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('products', models.ManyToManyField(to='products.Product')),
                ('team_leader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.profile')),
            ],
        ),
    ]