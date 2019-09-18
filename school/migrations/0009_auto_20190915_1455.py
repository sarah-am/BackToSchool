# Generated by Django 2.2.4 on 2019-09-15 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0008_auto_20190913_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(choices=[('P', 'Present'), ('A', 'Absent'), ('L', 'Late')], max_length=1),
        ),
    ]
