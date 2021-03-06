# Generated by Django 2.1.4 on 2019-01-03 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('teacher_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Section ID')),
                ('teacher_name', models.CharField(max_length=100, verbose_name='Teacher name')),
                ('teacher_name_ar', models.CharField(max_length=100, unique=True, verbose_name='Teacher name (arabic)')),
                ('teacher_mobile', models.IntegerField(verbose_name='Teacher mobile')),
                ('teacher_email', models.EmailField(default='', max_length=500, verbose_name='Teacher Email')),
            ],
            options={
                'verbose_name': 'Teacher',
                'verbose_name_plural': 'Teachers',
                'ordering': ['teacher_name', 'teacher_name_ar'],
            },
        ),
        migrations.AddIndex(
            model_name='teacher',
            index=models.Index(fields=['teacher_name'], name='HR_teacher_teacher_ef9d47_idx'),
        ),
        migrations.AddIndex(
            model_name='teacher',
            index=models.Index(fields=['teacher_name_ar'], name='HR_teacher_teacher_c57723_idx'),
        ),
        migrations.AddIndex(
            model_name='teacher',
            index=models.Index(fields=['teacher_email'], name='HR_teacher_teacher_15e4e5_idx'),
        ),
    ]
