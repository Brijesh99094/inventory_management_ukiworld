# Generated by Django 3.0.7 on 2021-04-14 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_purchase_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(null=True),
        ),
    ]
