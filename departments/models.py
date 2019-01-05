# -*- coding: utf-8 -*-

from django.db import models
from HR.models import Teacher
from courses.models import Course
from periods.models import Semester


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


class Section(models.Model):
    section_id = models.AutoField(primary_key=True, verbose_name="Section ID")
    section_code = models.IntegerField(unique=True, verbose_name="Section Code")
    section_department = models.ForeignKey(Department, verbose_name="Section Department", null=True,
                                           blank=True, on_delete=models.CASCADE)
    section_course = models.ForeignKey(Course, verbose_name="Section Course", null=True,
                                       blank=True, on_delete=models.CASCADE)
    section_semester = models.ForeignKey(Semester, verbose_name="Section Semester", null=True,
                                         blank=True, on_delete=models.CASCADE)
    section_teachers = models.ManyToManyField(Teacher, verbose_name="Section Teachers",
                                              blank=True)

    def __str__(self):
        return '[' + str(
            self.section_code) + '] ' + self.section_course.__str__()

    class Meta:
        ordering = ['section_code', 'section_course', ]
        verbose_name_plural = "Sections"
        verbose_name = "Section"
        indexes = [
            models.Index(fields=['section_code', ]),
        ]
