# Generated by Django 3.0.4 on 2020-07-08 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chartshow', '0005_auto_20200709_0000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worklist',
            name='pre_date',
        ),
        migrations.RemoveField(
            model_name='worklist',
            name='this_date',
        ),
    ]
