# Generated by Django 3.0.7 on 2021-06-06 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0017_auto_20210606_0337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='payment_type',
            field=models.CharField(max_length=50),
        ),
    ]