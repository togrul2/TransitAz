# Generated by Django 3.2.9 on 2021-12-07 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0011_auto_20211207_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='coords',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
