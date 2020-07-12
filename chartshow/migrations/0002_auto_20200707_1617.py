# Generated by Django 3.0.4 on 2020-07-07 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chartshow', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worklist',
            name='bug',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='worklist',
            name='owner',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='worklist',
            name='row_id',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
