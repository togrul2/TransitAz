# Generated by Django 3.2.9 on 2021-12-08 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0014_auto_20211207_2307'),
    ]

    operations = [
        migrations.AddField(
            model_name='transport',
            name='arrives_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
