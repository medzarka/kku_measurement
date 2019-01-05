# Generated by Django 2.1.4 on 2019-01-03 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeneratedDocument',
            fields=[
                ('generated_document_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Generated Document ID')),
                ('generated_document_description', models.CharField(blank=True, max_length=255, verbose_name='Generated Document Description')),
                ('generated_document_document', models.FileField(upload_to='data/generated', verbose_name='Generated Document Path')),
                ('generated_document_generated_at', models.DateTimeField(auto_now_add=True, verbose_name='Generated Document Time')),
            ],
            options={
                'verbose_name': 'Generated Document',
                'verbose_name_plural': 'Generated Documents',
                'ordering': ['generated_document_generated_at', 'generated_document_document'],
            },
        ),
        migrations.CreateModel(
            name='UploadDocument',
            fields=[
                ('upload_document_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Upload Document ID')),
                ('upload_document_description', models.CharField(blank=True, max_length=255, verbose_name='Upload Document Description')),
                ('upload_document_document', models.FileField(upload_to='data/upload', verbose_name='Upload Document Path')),
                ('upload_document_uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='Upload Document Time')),
            ],
            options={
                'verbose_name': 'Upload Document',
                'verbose_name_plural': 'Upload Documents',
                'ordering': ['upload_document_uploaded_at', 'upload_document_document'],
            },
        ),
        migrations.AddIndex(
            model_name='uploaddocument',
            index=models.Index(fields=['upload_document_document'], name='importManag_upload__ce620f_idx'),
        ),
        migrations.AddIndex(
            model_name='uploaddocument',
            index=models.Index(fields=['upload_document_uploaded_at'], name='importManag_upload__907d96_idx'),
        ),
        migrations.AddIndex(
            model_name='generateddocument',
            index=models.Index(fields=['generated_document_document'], name='importManag_generat_821b45_idx'),
        ),
        migrations.AddIndex(
            model_name='generateddocument',
            index=models.Index(fields=['generated_document_generated_at'], name='importManag_generat_4d7882_idx'),
        ),
    ]
