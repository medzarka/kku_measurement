# -*- coding: utf-8 -*-

from django.contrib import admin


from .models import College
from .models import Department
from .models import Section
from .models import Location

from periods.models import Semester


class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_name_ar', 'location_name')
    search_fields = ('location_name_ar', 'location_name')


class CollegeAdmin(admin.ModelAdmin):
    list_display = ('college_name', 'college_location')
    search_fields = ('college_name', 'college_location')
    list_filter = ('college_location__location_name',)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_name', 'department_location')
    search_fields = ('department_name', 'department_location__college_name')
    list_filter = ('department_location__college_name',)


class SectionAdmin(admin.ModelAdmin):
    list_display = ('section_code', 'section_course', 'section_department',)
    search_fields = ('section_code', 'section_course', 'section_department', 'section_semester',)
    list_filter = ('section_department', 'section_semester', 'section_course')

    def queryset(self, request, queryset):
        try:
            semester = Semester.objects.get(semester_isInUse=True)[0]
            queryset = queryset.filter(section_semester=semester)
            return queryset
        except:
            return queryset


# Register your models here.

admin.site.register(Location, LocationAdmin)
admin.site.register(College, CollegeAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Section, SectionAdmin)
