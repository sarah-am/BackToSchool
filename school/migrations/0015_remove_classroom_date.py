# Generated by Django 2.2.4 on 2019-09-21 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0014_auto_20190921_1312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroom',
            name='date',
        ),
    ]
