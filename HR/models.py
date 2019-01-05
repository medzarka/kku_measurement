# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True, verbose_name="Section ID")
    teacher_name = models.CharField(max_length=100, verbose_name="Teacher name")
    teacher_name_ar = models.CharField(max_length=100, unique=True, verbose_name="Teacher name (arabic)")
    teacher_mobile = models.BigIntegerField(verbose_name="Teacher mobile")
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
