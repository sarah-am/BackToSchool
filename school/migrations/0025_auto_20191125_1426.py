# Generated by Django 2.2.4 on 2019-11-25 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0024_remove_attendance_upload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(choices=[('P', 'Present'), ('A', 'Absent'), ('L', 'Late')], default='P', max_length=1),
        ),
    ]