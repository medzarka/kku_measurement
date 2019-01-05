# Generated by Django 2.1.4 on 2019-01-03 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('measurement', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='college',
            name='college_location',
        ),
        migrations.RemoveField(
            model_name='course',
            name='course_department',
        ),
        migrations.RemoveField(
            model_name='department',
            name='department_location',
        ),
        migrations.RemoveField(
            model_name='section',
            name='section_course',
        ),
        migrations.RemoveField(
            model_name='section',
            name='section_teachers',
        ),
        migrations.DeleteModel(
            name='Translation',
        ),
        migrations.AlterField(
            model_name='coursedocrequest',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='Course'),
        ),
        migrations.AlterField(
            model_name='sectiondocrequest',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='the_section', to='departments.Section', verbose_name='Section'),
        ),
        migrations.DeleteModel(
            name='College',
        ),
        migrations.DeleteModel(
            name='Course',
        ),
        migrations.DeleteModel(
            name='Department',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
        migrations.DeleteModel(
            name='Section',
        ),
        migrations.DeleteModel(
            name='Teacher',
        ),
    ]
