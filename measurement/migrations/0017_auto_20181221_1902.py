# Generated by Django 2.1.4 on 2018-12-21 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('measurement', '0016_auto_20181221_1842'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sectiondocrequest',
            options={'ordering': ['section'], 'verbose_name': 'Course Analysis Report', 'verbose_name_plural': 'Course Analysis Reports'},
        ),
        migrations.RemoveField(
            model_name='sectiondocrequest',
            name='college',
        ),
        migrations.RemoveField(
            model_name='sectiondocrequest',
            name='course',
        ),
        migrations.RemoveField(
            model_name='sectiondocrequest',
            name='department',
        ),
        migrations.AddField(
            model_name='teacher',
            name='teacher_email',
            field=models.EmailField(default='', max_length=500, verbose_name='Teacher Email'),
        ),
        migrations.AlterField(
            model_name='sectiondocrequest',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='measurement.Section', verbose_name='Section'),
        ),
    ]
