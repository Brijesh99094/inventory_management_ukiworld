# Generated by Django 3.0.7 on 2021-04-14 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_saleshasproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='phone',
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateField(null=True),
        ),
    ]