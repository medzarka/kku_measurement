# Generated by Django 2.1.4 on 2019-01-03 13:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('college_id', models.AutoField(primary_key=True, serialize=False, verbose_name='College ID')),
                ('college_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='College Name')),
                ('college_name_ar', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='College Name (Arabic)')),
            ],
            options={
                'verbose_name': 'College',
                'verbose_name_plural': 'Colleges',
                'ordering': ['college_name', 'college_location'],
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Course ID')),
                ('course_code', models.CharField(max_length=20, unique=True, verbose_name='Course Code')),
                ('course_name', models.CharField(max_length=100, verbose_name='Course Name')),
                ('course_name_ar', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Course Name (arabic)')),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
                'ordering': ['course_department', 'course_code', 'course_name', 'course_name_ar'],
            },
        ),
        migrations.CreateModel(
            name='CourseDocRequest',
            fields=[
                ('course_doc_id', models.AutoField(primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('doc_mean', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('doc_std_deviation', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('doc_skewness', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('doc_correlation', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('doc_max', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('doc_min', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('histogram', models.FileField(max_length=1024, upload_to='data/media/')),
                ('doc_ttest_annova_type', models.CharField(max_length=100, unique=True, verbose_name='Correlation Type')),
                ('doc_ttest_annova_value', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, verbose_name='Course Correlation Value')),
                ('doc_ttest_annova_sig', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True, verbose_name='Course Correlation Significance')),
                ('doc_explanation', models.TextField(verbose_name='\u202b\u202aExplanation\u202c\u202c \u202b\u202aand\u202c\u202c \u202b\u202athe\u202c\u202c \u202b\u202arecommendations\u202c\u202c')),
            ],
            options={
                'verbose_name': 'Course Analysis Report',
                'verbose_name_plural': 'Course Analysis Reports',
                'ordering': ['course'],
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('department_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Department ID')),
                ('department_name', models.CharField(max_length=100, verbose_name='Department Name')),
                ('department_name_ar', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Department Name (Arabic)')),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
                'ordering': ['department_name', 'department_location'],
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('location_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Location ID')),
                ('location_name_ar', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='location Name (arabic)')),
                ('location_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='location Name')),
            ],
            options={
                'verbose_name': 'Location',
                'verbose_name_plural': 'Locations',
                'ordering': ['location_name'],
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('section_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Section ID')),
                ('section_code', models.IntegerField(unique=True, verbose_name='Section Code')),
            ],
            options={
                'verbose_name': 'Section',
                'verbose_name_plural': 'Sections',
                'ordering': ['section_course', 'section_code'],
            },
        ),
        migrations.CreateModel(
            name='SectionDocRequest',
            fields=[
                ('section_doc_id', models.AutoField(primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('maxgrades', models.IntegerField(default=100, verbose_name='Full Grade')),
                ('student_grades', models.CharField(max_length=2048, verbose_name='Grades')),
                ('doc_mean', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('doc_std_deviation', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('doc_skewness', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('doc_correlation', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('doc_max', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('doc_min', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('histogram', models.FileField(max_length=1024, upload_to='data/media/')),
                ('doc_explanation', models.TextField(verbose_name='\u202b\u202aExplanation\u202c\u202c \u202b\u202aand\u202c\u202c \u202b\u202athe\u202c\u202c \u202b\u202arecommendations\u202c\u202c')),
            ],
            options={
                'verbose_name': 'Section Analysis Report',
                'verbose_name_plural': 'Section Analysis Reports',
                'ordering': ['section'],
            },
        ),
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
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('translation_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Section ID')),
                ('translation_ar', models.CharField(max_length=100, unique=True, verbose_name='Translation AR')),
                ('translation_en', models.CharField(blank=True, max_length=100, null=True, verbose_name='Translation EN')),
            ],
            options={
                'verbose_name': 'Translation',
                'verbose_name_plural': 'Translations',
                'ordering': ['translation_ar'],
            },
        ),
        migrations.AddIndex(
            model_name='translation',
            index=models.Index(fields=['translation_ar'], name='measurement_transla_8c2a76_idx'),
        ),
        migrations.AddIndex(
            model_name='translation',
            index=models.Index(fields=['translation_en'], name='measurement_transla_cc6d7a_idx'),
        ),
        migrations.AddIndex(
            model_name='teacher',
            index=models.Index(fields=['teacher_name'], name='measurement_teacher_18300e_idx'),
        ),
        migrations.AddIndex(
            model_name='teacher',
            index=models.Index(fields=['teacher_name_ar'], name='measurement_teacher_cdfe67_idx'),
        ),
        migrations.AddIndex(
            model_name='teacher',
            index=models.Index(fields=['teacher_email'], name='measurement_teacher_e22624_idx'),
        ),
        migrations.AddField(
            model_name='sectiondocrequest',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='the_section', to='measurement.Section', verbose_name='Section'),
        ),
        migrations.AddField(
            model_name='section',
            name='section_course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='the_course', to='measurement.Course', verbose_name='Section Course'),
        ),
        migrations.AddField(
            model_name='section',
            name='section_teachers',
            field=models.ManyToManyField(blank=True, to='measurement.Teacher', verbose_name='Section Teachers'),
        ),
        migrations.AddIndex(
            model_name='location',
            index=models.Index(fields=['location_name_ar'], name='measurement_locatio_401a3b_idx'),
        ),
        migrations.AddIndex(
            model_name='location',
            index=models.Index(fields=['location_name'], name='measurement_locatio_1fa6ec_idx'),
        ),
        migrations.AddField(
            model_name='department',
            name='department_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='measurement.College', verbose_name='Department Location'),
        ),
        migrations.AddField(
            model_name='coursedocrequest',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='measurement.Course', verbose_name='Course'),
        ),
        migrations.AddField(
            model_name='course',
            name='course_department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='measurement.Department', verbose_name='Course Department'),
        ),
        migrations.AddField(
            model_name='college',
            name='college_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='measurement.Location', verbose_name='College Location'),
        ),
        migrations.AddIndex(
            model_name='sectiondocrequest',
            index=models.Index(fields=['section'], name='measurement_section_513290_idx'),
        ),
        migrations.AddIndex(
            model_name='section',
            index=models.Index(fields=['section_code'], name='measurement_section_2bd634_idx'),
        ),
        migrations.AddIndex(
            model_name='department',
            index=models.Index(fields=['department_name'], name='measurement_departm_df1508_idx'),
        ),
        migrations.AddIndex(
            model_name='department',
            index=models.Index(fields=['department_name_ar'], name='measurement_departm_961b50_idx'),
        ),
        migrations.AddIndex(
            model_name='coursedocrequest',
            index=models.Index(fields=['course'], name='measurement_course__860b9c_idx'),
        ),
        migrations.AddIndex(
            model_name='course',
            index=models.Index(fields=['course_code'], name='measurement_course__1121a4_idx'),
        ),
        migrations.AddIndex(
            model_name='course',
            index=models.Index(fields=['course_name'], name='measurement_course__be593e_idx'),
        ),
        migrations.AddIndex(
            model_name='course',
            index=models.Index(fields=['course_name_ar'], name='measurement_course__6ec2f3_idx'),
        ),
        migrations.AddIndex(
            model_name='college',
            index=models.Index(fields=['college_name'], name='measurement_college_d1ea94_idx'),
        ),
        migrations.AddIndex(
            model_name='college',
            index=models.Index(fields=['college_name_ar'], name='measurement_college_e2950c_idx'),
        ),
    ]
