# Generated by Django 2.2.4 on 2019-09-06 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0004_auto_20190904_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semester',
            name='season',
            field=models.CharField(choices=[('Fall', 'Fall'), ('Spring', 'Spring'), ('Summer', 'Summer')], max_length=6),
        ),
    ]
