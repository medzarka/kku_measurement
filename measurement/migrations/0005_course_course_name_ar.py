# Generated by Django 2.1.4 on 2018-12-16 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('measurement', '0004_auto_20181216_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_name_ar',
            field=models.CharField(default='', max_length=100, unique=True, verbose_name='Course Name (arabic)'),
        ),
    ]
