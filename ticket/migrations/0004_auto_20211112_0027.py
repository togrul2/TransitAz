# Generated by Django 3.2.9 on 2021-11-11 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0003_auto_20211112_0025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='busstation',
            name='map_x',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='busstation',
            name='map_y',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
