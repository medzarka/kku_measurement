# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Speciality(models.Model):
    speciality_id = models.AutoField(primary_key=True, verbose_name="ID")
    speciality_name = models.CharField(max_length=50, verbose_name="Name", blank=False, null=False, default='')
    speciality_name_ar = models.CharField(max_length=50, verbose_name="Arabic Name", blank=False, null=False, default='')

    def __str__(self):
        return self.speciality_name

    class Meta:
        ordering = ["speciality_name"]
        verbose_name_plural = "Specialities"
        verbose_name = "Speciality"


class AcademicLevel(models.Model):
    academic_level_id = models.AutoField(primary_key=True, verbose_name="ID")
    academic_level_name = models.CharField(max_length=50, verbose_name="Name", blank=False, null=False)

    def __str__(self):
        return self.academic_level_name

    class Meta:
        ordering = ["academic_level_name"]
        verbose_name_plural = "Academic Levels"
        verbose_name = "Academic Level"

class Course(models.Model):
    course_id = models.AutoField(primary_key=True, verbose_name="ID")
    course_code = models.CharField(max_length=20, unique=True, verbose_name="Code")
    course_name = models.CharField(max_length=100, verbose_name="Name")
    course_name_ar = models.CharField(max_length=100, verbose_name="Arabic Name", default='')
    course_theory_load = models.IntegerField(verbose_name="Theory Load", blank=False, null=False, default=0)
    course_lab_load = models.IntegerField(verbose_name="Lab Load", blank=False, null=False, default=0)
    course_tutorial_load = models.IntegerField(verbose_name="Tutorial Load", blank=False, null=False, default=0)
    speciality = models.ForeignKey('Speciality', on_delete=models.CASCADE)
    academic_level = models.ForeignKey('AcademicLevel', on_delete=models.CASCADE)

    def __str__(self):
        return '['+self.course_code + "] " + self.course_name

    class Meta:
        ordering = ['course_code', 'speciality', 'academic_level']
        verbose_name_plural = "Courses"
        verbose_name = "Course"
