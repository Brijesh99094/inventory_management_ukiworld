# Generated by Django 3.0.7 on 2021-05-04 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0012_auto_20210504_0906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleshasproduct',
            name='imei_no',
            field=models.BigIntegerField(null=True),
        ),
    ]