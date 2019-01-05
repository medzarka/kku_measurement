# Generated by Django 2.1.4 on 2019-01-03 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importManager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generateddocument',
            name='generated_document_document',
            field=models.FileField(upload_to='documents/generated', verbose_name='Generated Document Path'),
        ),
        migrations.AlterField(
            model_name='uploaddocument',
            name='upload_document_document',
            field=models.FileField(upload_to='documents/upload', verbose_name='Upload Document Path'),
        ),
    ]
