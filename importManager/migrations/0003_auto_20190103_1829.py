# Generated by Django 2.1.4 on 2019-01-03 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importManager', '0002_auto_20190103_1528'),
    ]

    operations = [
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('translation_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Section ID')),
                ('translation_ar', models.CharField(max_length=500, unique=True, verbose_name='Translation AR')),
                ('translation_en', models.CharField(blank=True, max_length=500, null=True, verbose_name='Translation EN')),
            ],
            options={
                'verbose_name': 'Translation',
                'verbose_name_plural': 'Translations',
                'ordering': ['translation_ar'],
            },
        ),
        migrations.AddIndex(
            model_name='translation',
            index=models.Index(fields=['translation_ar'], name='importManag_transla_baf69d_idx'),
        ),
        migrations.AddIndex(
            model_name='translation',
            index=models.Index(fields=['translation_en'], name='importManag_transla_479b42_idx'),
        ),
    ]
