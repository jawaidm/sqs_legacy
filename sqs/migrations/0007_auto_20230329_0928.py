# Generated by Django 3.2.4 on 2023-03-29 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sqs', '0006_auto_20230328_1706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='layeraccesslog',
            name='layer',
        ),
        migrations.AddField(
            model_name='layeraccesslog',
            name='layer_name',
            #field=models.CharField(default='a', max_length=64),
            field=models.CharField(max_length=64),
            preserve_default=False,
        ),
    ]
