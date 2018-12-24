# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone


###################################################################################################################
###################################################################################################################
class Location(models.Model):
    location_id = models.AutoField(primary_key=True, verbose_name="Location ID")
    location_name_ar = models.CharField(max_length=100, unique=True, verbose_name="location Name (arabic)", null=True,
                                        blank=True)
    location_name = models.CharField(max_length=100, verbose_name="location Name", null=True, blank=True)

    def __str__(self):
        return self.location_name

    class Meta:
        ordering = ['location_name', ]
        verbose_name_plural = "Locations"
        verbose_name = "Location"
        indexes = [
            models.Index(fields=['location_name_ar', ]),
            models.Index(fields=['location_name', ]),
        ]


class College(models.Model):
    college_id = models.AutoField(primary_key=True, verbose_name="College ID")
    college_name = models.CharField(max_length=100, verbose_name="College Name", null=True, blank=True)
    college_name_ar = models.CharField(max_length=100, unique=True, verbose_name="College Name (Arabic)", null=True,
                                       blank=True)
    college_location = models.ForeignKey(Location, verbose_name="College Location", null=True, blank=True,
                                         on_delete=models.CASCADE)

    def __str__(self):
        return self.college_name + '[' + self.college_location.__str__() + ']'

    class Meta:
        ordering = ['college_name', 'college_location']
        verbose_name_plural = "Colleges"
        verbose_name = "College"
        indexes = [
            models.Index(fields=['college_name', ]),
            models.Index(fields=['college_name_ar', ]),
        ]


class Department(models.Model):
    department_id = models.AutoField(primary_key=True, verbose_name="Department ID")
    department_name = models.CharField(max_length=100, verbose_name="Department Name")
    department_name_ar = models.CharField(max_length=100, unique=True, null=True, blank=True,
                                          verbose_name="Department Name (Arabic)")
    department_location = models.ForeignKey(College, verbose_name="Department Location",
                                            null=True, on_delete=models.CASCADE,
                                            blank=True)

    def __str__(self):
        return self.department_name

    class Meta:
        ordering = ['department_name', 'department_location']
        verbose_name_plural = "Departments"
        verbose_name = "Department"
        indexes = [
            models.Index(fields=['department_name', ]),
            models.Index(fields=['department_name_ar', ]),
        ]


class Course(models.Model):
    course_id = models.AutoField(primary_key=True, verbose_name="Course ID")
    course_code = models.CharField(max_length=20, unique=True, verbose_name="Course Code")
    course_name = models.CharField(max_length=100, verbose_name="Course Name")
    course_name_ar = models.CharField(max_length=100, null=True, blank=True, verbose_name="Course Name (arabic)",
                                      default='')
    course_department = models.ForeignKey(Department, verbose_name="Course Department",
                                          null=True, on_delete=models.CASCADE,
                                          blank=True)

    def __str__(self):
        return '[' + self.course_code + '] ' + self.course_name

    class Meta:
        ordering = ['course_department', 'course_code', 'course_name', 'course_name_ar']
        verbose_name_plural = "Courses"
        verbose_name = "Course"
        indexes = [
            models.Index(fields=['course_code', ]),
            models.Index(fields=['course_name', ]),
            models.Index(fields=['course_name_ar', ]),
        ]


class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True, verbose_name="Section ID")
    teacher_name = models.CharField(max_length=100, verbose_name="Teacher name")
    teacher_name_ar = models.CharField(max_length=100, unique=True, verbose_name="Teacher name (arabic)")
    teacher_mobile = models.IntegerField(verbose_name="Teacher mobile")
    teacher_email = models.EmailField(max_length=500, null=False, blank=False, verbose_name='Teacher Email', default='')

    def __str__(self):
        return self.teacher_name + ' ----- ' + self.teacher_name_ar

    class Meta:
        ordering = ['teacher_name', 'teacher_name_ar']
        verbose_name_plural = "Teachers"
        verbose_name = "Teacher"
        indexes = [
            models.Index(fields=['teacher_name', ]),
            models.Index(fields=['teacher_name_ar', ]),
            models.Index(fields=['teacher_email', ]),
        ]


class Section(models.Model):
    section_id = models.AutoField(primary_key=True, verbose_name="Section ID")
    section_code = models.IntegerField(unique=True, verbose_name="Section Code")
    section_course = models.ForeignKey(Course, verbose_name="Section Course", null=True,
                                       blank=True, on_delete=models.CASCADE, related_name = 'the_course')
    section_teachers = models.ManyToManyField(Teacher, verbose_name="Section Teachers",
                                              blank=True)

    def __str__(self):
        return '[' + str(
            self.section_code) + '] ' + self.section_course.__str__()

    class Meta:
        ordering = ['section_course', 'section_code']
        verbose_name_plural = "Sections"
        verbose_name = "Section"
        indexes = [
            models.Index(fields=['section_code', ]),
        ]


class Translation(models.Model):
    translation_id = models.AutoField(primary_key=True, verbose_name="Section ID")
    translation_ar = models.CharField(max_length=100, unique=True, verbose_name="Translation AR")
    translation_en = models.CharField(max_length=100, verbose_name="Translation EN", null=True,
                                      blank=True)

    def __str__(self):
        return self.translation_ar

    class Meta:
        ordering = ['translation_ar', ]
        verbose_name_plural = "Translations"
        verbose_name = "Translation"
        indexes = [
            models.Index(fields=['translation_ar', ]),
            models.Index(fields=['translation_en', ]),
        ]


####################################################################################################
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
        verbose_name_plural = "Section Analysis Reports"
        verbose_name = "Section Analysis Report"
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
    doc_ttest_annova_type = models.CharField(max_length=100, unique=True, verbose_name="Correlation Type")
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
        verbose_name_plural = "Course Analysis Reports"
        verbose_name = "Course Analysis Report"
        indexes = [
            models.Index(fields=['course', ]),
        ]