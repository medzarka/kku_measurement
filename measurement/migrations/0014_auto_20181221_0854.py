# Generated by Django 2.1.4 on 2018-12-21 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('measurement', '0013_translation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translation',
            name='translation_en',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Translation EN'),
        ),
    ]