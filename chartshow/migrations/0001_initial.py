# Generated by Django 3.0.4 on 2020-07-23 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('owner_id', models.AutoField(primary_key=True, serialize=False)),
                ('owner', models.CharField(max_length=100)),
                ('active', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='WorkList',
            fields=[
                ('row_id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('owner', models.CharField(max_length=100)),
                ('mid', models.CharField(max_length=50)),
                ('bug', models.CharField(max_length=50, null=True)),
                ('procedure', models.CharField(max_length=200)),
                ('room', models.CharField(max_length=50, null=True)),
                ('status', models.CharField(max_length=50, null=True)),
                ('progress', models.CharField(max_length=50, null=True)),
                ('hours', models.CharField(max_length=50, null=True)),
                ('progress_delta', models.CharField(max_length=50, null=True)),
                ('hours_delta', models.CharField(max_length=50, null=True)),
                ('modified_at', models.DateField()),
                ('active', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Flowchart_mid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.CharField(max_length=10)),
                ('col', models.CharField(max_length=10)),
                ('owner', models.CharField(max_length=100)),
                ('mid', models.CharField(max_length=50)),
                ('bug', models.CharField(max_length=50, null=True)),
                ('procedure', models.CharField(max_length=200)),
                ('room', models.CharField(max_length=50, null=True)),
                ('status', models.CharField(max_length=50, null=True)),
                ('progress', models.CharField(max_length=50, null=True)),
                ('hours', models.CharField(max_length=50, null=True)),
                ('progress_delta', models.CharField(max_length=50, null=True)),
                ('hours_delta', models.CharField(max_length=50, null=True)),
                ('modified_at', models.DateField()),
                ('active', models.BooleanField()),
                ('background_group', models.CharField(max_length=50, null=True)),
                ('test_type', models.CharField(max_length=50, null=True)),
                ('ccp', models.CharField(max_length=10, null=True)),
            ],
            options={
                'unique_together': {('row', 'col', 'room')},
            },
        ),
    ]
