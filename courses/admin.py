# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from .models import Speciality
from .models import AcademicLevel
from .models import Course



class SpecialityAdmin(admin.ModelAdmin):
    list_display = ('speciality_name', 'speciality_name_ar')
    search_fields = ('speciality_name', 'speciality_name', 'speciality_name_ar')


class AcademicLevelAdmin(admin.ModelAdmin):
    list_display = ('academic_level_name', )
    search_fields = ('academic_level_name', )


class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'course_code', 'course_name', 'speciality', 'academic_level', 'course_theory_load', 'course_lab_load',
        'course_tutorial_load')
    search_fields = ('course_code', 'course_name', 'speciality', 'academic_level')
    list_filter = ('speciality', 'academic_level')


# Register your models here.
admin.site.register(Speciality, SpecialityAdmin)
admin.site.register(AcademicLevel, AcademicLevelAdmin)
admin.site.register(Course, CourseAdmin)

