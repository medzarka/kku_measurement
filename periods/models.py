# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date
from django.db import models
from django.contrib import admin
from datetime import datetime
from django import forms

from django.core.exceptions import ValidationError


# Create your models here.


class AcademicYear(models.Model):
    academic_year_id = models.AutoField(primary_key=True, verbose_name="Academic Year ID")
    academic_year_name = models.CharField(max_length=50, verbose_name="Academic Year Name", blank=False, null=False)
    academic_year_date_start = models.DateField(verbose_name="Academic Year Start Date", blank=False,
                                                null=False)
    academic_year_date_end = models.DateField(verbose_name="Academic Year End Date", blank=False,
                                              null=False)

    @property
    def isActualAcademicYear(self):
        present = date.today()
        if present >= self.academic_year_date_start and present <= self.academic_year_date_end:
            return True
        else:
            return False

    def __str__(self):
        _start = self.academic_year_date_start.strftime("%A %d. %B %Y")
        _end = self.academic_year_date_end.strftime("%A %d. %B %Y")
        return self.academic_year_name

    class Meta:
        ordering = ["academic_year_date_start"]
        verbose_name_plural = "Academic Years"
        verbose_name = "Academic Year"


class Semester(models.Model):
    semester_id = models.AutoField(primary_key=True, verbose_name="Semester ID")
    semester_name = models.CharField(max_length=50, verbose_name="Name", blank=False, null=False)
    semester_academic_year = models.ForeignKey('AcademicYear', on_delete=models.CASCADE)
    semester_date_start = models.DateField(verbose_name="Start Date", blank=False,
                                           null=False)
    semester_date_end = models.DateField(verbose_name="End Date", blank=False,
                                         null=False)
    semester_isSummerTerm = models.BooleanField(verbose_name="Is Summer Term", blank=False)
    semester_isInUse = models.BooleanField(verbose_name="Is in Use", blank=False)

    @property
    def isActualSemester(self):
        present = date.today()
        if present >= self.semester_date_start and present <= self.semester_date_end:
            return True
        else:
            return False

    def __str__(self):
        _start = self.semester_date_start.strftime("%A %d. %B %Y")
        _end = self.semester_date_end.strftime("%A %d. %B %Y")
        return self.semester_name + "  -  " + self.semester_academic_year.academic_year_name

    class Meta:
        ordering = ["semester_academic_year", "semester_name"]
        verbose_name_plural = "Semesters"
        verbose_name = "Semester"
