# Generated by Django 3.0.4 on 2020-07-07 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chartshow', '0002_auto_20200707_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worklist',
            name='hours',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='worklist',
            name='hours_delta',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='worklist',
            name='progress',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='worklist',
            name='progress_delta',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='worklist',
            name='room',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='worklist',
            name='status',
            field=models.CharField(max_length=50, null=True),
        ),
    ]