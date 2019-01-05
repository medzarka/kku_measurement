# Generated by Django 2.1.4 on 2019-01-05 09:17

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0001_initial'),
        ('courses', '0003_auto_20190104_2042'),
        ('measurement', '0003_auto_20190104_2149'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseAnalysisReport',
            fields=[
                ('course_analysis_report_id', models.AutoField(primary_key=True, serialize=False)),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('file', models.FileField(max_length=1024, upload_to='data/media/Measurements/Courses')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='Course')),
            ],
            options={
                'verbose_name': 'Course Analysis Report',
                'verbose_name_plural': 'Course Analysis Reports',
                'ordering': ['course'],
            },
        ),
        migrations.CreateModel(
            name='SectionAnalysisReport',
            fields=[
                ('section_analysis_report_id', models.AutoField(primary_key=True, serialize=False)),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('file', models.FileField(max_length=1024, upload_to='data/media/Measurements/Sections')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='departments.Section', verbose_name='Section')),
            ],
            options={
                'verbose_name': 'Section Analysis Report',
                'verbose_name_plural': 'Section Analysis Reports',
                'ordering': ['section'],
            },
        ),
        migrations.AlterModelOptions(
            name='coursedocrequest',
            options={'ordering': ['course'], 'verbose_name': 'Course Analysis Measurement', 'verbose_name_plural': 'Course Analysis Measurements'},
        ),
        migrations.AlterModelOptions(
            name='sectiondocrequest',
            options={'ordering': ['section'], 'verbose_name': 'Section Analysis Measurement', 'verbose_name_plural': 'Section Analysis Measurements'},
        ),
        migrations.AddIndex(
            model_name='sectionanalysisreport',
            index=models.Index(fields=['section'], name='measurement_section_4b1676_idx'),
        ),
        migrations.AddIndex(
            model_name='courseanalysisreport',
            index=models.Index(fields=['course'], name='measurement_course__34d390_idx'),
        ),
    ]