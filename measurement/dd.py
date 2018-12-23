# -*- coding: utf-8 -*-

import xlrd as xl
from googletrans import Translator

from models import Location
from models import College
from models import Department
from models import Course
from models import Teacher


def handle_teacher(teacher_name, teacher_name_ar, teacher_mobile):
    try:
        obj = Teacher.objects.get(teacher_name_ar=teacher_name_ar)
        if(obj == None):
            obj = Teacher()
        obj.teacher_name_ar = teacher_name_ar
        obj.teacher_name = teacher_name
        obj.teacher_mobile =teacher_mobile
        obj.save()
        return True
    except:
        return False

__file = 'ZARKA.xlsx'
workbook = xl.open_workbook(__file, on_demand=True, encoding_override='UTF8')
worksheet = workbook.sheet_by_index(0)

___line = 0
_____location_ar = ''
_____location_en = ''
_____college_ar = ''
_____college_en = ''
_____department_ar = ''
_____department_en = ''
_____course_ar=''
_____course_en=''
_____course_code=''
_____teacher = ''
_____section = 0

translator = Translator(service_urls=['translate.google.com.sa', ])

while True:
    try:
        tmp1 = worksheet.cell_value(___line, 2)
        tmp2 = worksheet.cell_value(___line, 1)
        tmp3 = worksheet.cell_value(___line, 3)

        if(tmp1 == 'المقر :' ):
            print("###########################################################")
            _____location_ar  = worksheet.cell_value(___line, 7)
            _trans = translator.translate(_____location_ar, dest='en')
            _____location_en = _trans.text
            print(u'Location = ' + _____location_ar)
            print('Location = ' + _____location_en)
        if (tmp1 == 'الكلية :'):
            _____college_ar = worksheet.cell_value(___line, 7)
            _trans = translator.translate(_____college_ar, dest='en')
            _____college_en = _trans.text
            print('\t------------------------------------')
            print(u'\tCollege = ' + _____college_en)
            print('\tCollege = ' + _____college_ar)
        if (tmp2 == 'القسم :'):
            _____department_ar = worksheet.cell_value(___line, 6)
            _trans = translator.translate(_____department_ar, dest='en')
            _____department_en = _trans.text
            print(u'\t\tDepartment =' + _____department_ar)
            print('\t\tDepartment =' + _____department_en)
        if (tmp3 == 'الشعبة'):
            ___line = ___line + 2
            __test = worksheet.cell_value(___line, 2)
            while(__test != 'المقر :'):
                _____course_ar = worksheet.cell_value(___line, 12)
                if _____course_ar != '':
                    _____course_code = worksheet.cell_value(___line, 9)
                    _trans = translator.translate(_____course_ar, dest='en')
                    _____course_en = _trans.text
                    _____teacher = worksheet.cell_value(___line, 8)
                    _____section = int(worksheet.cell_value(___line, 3))
                    print(u'\t\t\tCourse Code =' + _____course_code)
                    print(u'\t\t\tCourse =' + _____course_ar)
                    print('\t\t\tCourse =' + _____course_en)
                    print('\t\t\tSection =' + str(_____section))
                    print('\t\t\t\tTeacher =' + _____teacher)
                    _____teacher_name = _____teacher.split('-')[0]
                    _____teacher_phone = _____teacher.split('-')[1]
                    handle_teacher('', _____teacher_name, _____teacher_phone)

                else:
                    _____teacher = worksheet.cell_value(___line, 8)
                    print('\t\t\t\tTeacher =' + _____teacher)
                ___line = ___line + 1
                __test = worksheet.cell_value(___line, 2)

            ___line = ___line - 1




        ___line = ___line + 1





    except IndexError:
        break

