# Generated by Django 3.2.9 on 2021-12-02 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0007_auto_20211124_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bus',
            name='arrives_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='train',
            name='arrives_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
