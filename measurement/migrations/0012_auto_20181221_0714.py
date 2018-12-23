# Generated by Django 2.1.4 on 2018-12-21 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('measurement', '0011_location_location_name_ar'),
    ]

    operations = [
        migrations.AddField(
            model_name='college',
            name='college_name_ar',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='College Name (Arabic)'),
        ),
        migrations.AddField(
            model_name='department',
            name='department_name_ar',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Department Name (Arabic)'),
        ),
    ]
