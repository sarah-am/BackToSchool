# Generated by Django 2.2.4 on 2019-09-30 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0015_remove_classroom_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semester',
            name='year',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='student',
            name='dob',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.EmailField(max_length=70),
        ),
    ]