# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Teacher

class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'teacher_id', 'teacher_name', 'teacher_name_ar', 'teacher_mobile')
    search_fields = ('teacher_name', 'teacher_name_ar', 'teacher_mobile')

admin.site.register(Teacher, TeacherAdmin)