# Generated by Django 3.2.9 on 2021-11-21 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=2000)),
                ('region', models.CharField(max_length=50)),
                ('coords', models.CharField(max_length=100)),
                ('map_x', models.FloatField(blank=True, null=True)),
                ('map_y', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]
