# Generated by Django 3.0.7 on 2021-04-14 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_auto_20210414_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='phone',
            field=models.IntegerField(null=True),
        ),
    ]
