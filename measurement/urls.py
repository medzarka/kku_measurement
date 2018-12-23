# -*- coding: utf-8 -*-

from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('section', views.section, name="section_form"),
    path('course', views.course, name="course_form"),
    path('departement', views.department, name="department_form"),
    path('section/action', views.section_action, name="do_section"),
    path('section/docx', views.section_docx, name="section_docx"),
    path('couse/action', views.course_action, name="do_course"),
    path('department/action', views.department_action, name="do_department"),
]
