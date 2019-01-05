# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from departments.models import Section
from courses.models import Course


class SectionDocRequest(models.Model):
    section_doc_id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(default=timezone.now, null=False, blank=False)

    section = models.ForeignKey(Section, verbose_name="Section", on_delete=models.CASCADE, related_name = 'the_section')

    maxgrades = models.IntegerField(null=False, blank=False, verbose_name='Full Grade', default=100)
    student_grades = models.CharField(max_length=2048, null=False, blank=False, verbose_name='Grades')

    doc_mean = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    doc_std_deviation = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    doc_skewness = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    doc_correlation = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    doc_max = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    doc_min = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)

    histogram = models.FileField(upload_to='data/media/', max_length=1024, null=False, blank=False)

    doc_explanation = models.TextField(null=False, blank=False,
                                       verbose_name='‫‪Explanation‬‬ ‫‪and‬‬ ‫‪the‬‬ ‫‪recommendations‬‬')


    def __str__(self):
        return 'coursedoc id=' + str(
            self.section_doc_id) + "(Section= " + str(
            self.section) + ')'

    class Meta:
        ordering = ['section']
        verbose_name_plural = "Section Analysis Measurements"
        verbose_name = "Section Analysis Measurement"
        indexes = [
            models.Index(fields=['section', ]),
        ]

class CourseDocRequest(models.Model):
    course_doc_id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(default=timezone.now, null=False, blank=False)

    course = models.ForeignKey(Course, verbose_name="Course", on_delete=models.CASCADE)

    doc_mean = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    doc_std_deviation = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    doc_skewness = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    doc_correlation = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    doc_max = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    doc_min = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)

    histogram = models.FileField(upload_to='data/media/', max_length=1024, null=False, blank=False)
    doc_ttest_annova_type = models.CharField(max_length=100, verbose_name="Correlation Type")
    doc_ttest_annova_value = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name="Course Correlation Value")
    doc_ttest_annova_sig = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name="Course Correlation Significance")

    doc_explanation = models.TextField(null=False, blank=False,
                                       verbose_name='‫‪Explanation‬‬ ‫‪and‬‬ ‫‪the‬‬ ‫‪recommendations‬‬')


    def __str__(self):
        return 'coursedoc id=' + str(
            self.course_doc_id) + "(Course= " + str(
            self.course) + ')'

    class Meta:
        ordering = ['course']
        verbose_name_plural = "Course Analysis Measurements"
        verbose_name = "Course Analysis Measurement"
        indexes = [
            models.Index(fields=['course', ]),
        ]


class SectionAnalysisReport(models.Model):
    section_analysis_report_id = models.AutoField(primary_key=True)
    upload_date = models.DateTimeField(default=timezone.now, null=False, blank=False)
    section = models.ForeignKey(Section, verbose_name="Section", on_delete=models.CASCADE)
    file = models.FileField(upload_to='Measurements/Sections', max_length=1024, null=False, blank=False)
    remarks = models.TextField(null=False, blank=False, verbose_name='Remarks‬‬', default='')

    def __str__(self):
        return 'Section Report for the section ' + str(
            self.section.section_code) + "(Course= " + self.section.section_course.course_name+")"

    class Meta:
        ordering = ['section']
        verbose_name_plural = "Section Analysis Reports"
        verbose_name = "Section Analysis Report"
        indexes = [
            models.Index(fields=['section', ]),
        ]

class CourseAnalysisReport(models.Model):
    course_analysis_report_id = models.AutoField(primary_key=True)
    upload_date = models.DateTimeField(default=timezone.now, null=False, blank=False)
    course = models.ForeignKey(Course, verbose_name="Course", on_delete=models.CASCADE)
    file = models.FileField(upload_to='Measurements/Courses', max_length=1024, null=False, blank=False)
    remarks = models.TextField(null=False, blank=False, verbose_name='Remarks‬‬', default='')

    def __str__(self):
        return 'Course Report for = ' + self.course.course_name

    class Meta:
        ordering = ['course']
        verbose_name_plural = "Course Analysis Reports"
        verbose_name = "Course Analysis Report"
        indexes = [
            models.Index(fields=['course', ]),
        ]