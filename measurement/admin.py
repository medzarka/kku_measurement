from django.contrib import admin
from .models import SectionDocRequest
from .models import CourseDocRequest

from .models import Location
from .models import College
from .models import Department
from .models import Course
from .models import Teacher
from .models import Section
from .models import Translation

import xlrd as xl
import csv
from googletrans import Translator
from django.http import HttpResponse
from django.contrib import messages


def Translate(translation_ar):
    try:
        obj = Translation.objects.get(translation_ar=translation_ar)
        #print('Translation found with id = ' + str(obj.translation_id))
        return obj.translation_en

    except Translation.DoesNotExist:
        obj = Translation()
        #print('Translation not found, creating new object')
        translator = Translator(service_urls=['translate.google.com.sa', 'translate.google.com'])
        translation_en = translator.translate(translation_ar, dest='en').text
        obj.translation_ar = translation_ar
        obj.translation_en = translation_en
        try:
            obj.save()
            #print("Translation for " + translation_ar + ' saved in database')
            return obj.translation_en
        except Exception as e:
            print("Error in storing the Translation object")
            print(str(e))
            return None


def handle_location(_____location_ar, _____location_en):
    try:
        obj = Location.objects.get(location_name=_____location_en)
        #print('Location found with id = ' + str(obj.location_id))
    except Location.DoesNotExist:
        obj = Location()
        #print('Location not found, creating new object')
    obj.location_name = _____location_en
    obj.location_name_ar = _____location_ar

    try:
        obj.save()
        print("Location " + _____location_en + ' saved in database')
        return obj
    except:
        print("Error in storing the Location object")
        return None


def handle_college(college_name, college_name_ar, college_location):
    try:
        obj = College.objects.get(college_name=college_name)
        #print('College found with id = ' + str(obj.college_id))
    except College.DoesNotExist:
        obj = College()
        #print('College not found, creating new object')
    obj.college_name = college_name
    obj.college_name_ar = college_name_ar
    obj.college_location = college_location

    try:
        obj.save()
        #print("College " + college_name + ' saved in database')
        return obj
    except:
        print("Error in storing the College object")
        return None


def handle_department(department_name, department_name_ar, department_location):
    try:
        obj = Department.objects.get(department_name=department_name)
        #print('Department found with id = ' + str(obj.department_id))
    except Department.DoesNotExist:
        obj = Department()
        #print('College not found, creating new object')
    obj.department_name = department_name
    obj.department_name_ar = department_name_ar
    obj.department_location = department_location

    try:
        obj.save()
        #print("Department " + department_name + ' saved in database')
        return obj
    except:
        print("Error in storing the Department object")
        return None


def handle_course(course_code, course_name, course_name_ar, course_department):
    try:
        obj = Course.objects.get(course_code=course_code)
        print('Course found with id = ' + str(obj.course_id))
    except Course.DoesNotExist:
        obj = Course()
        print('Course not found, creating new object')
    obj.course_name = course_name
    obj.course_code = course_code
    obj.course_name_ar = course_name_ar
    obj.course_department = course_department

    #try:
    obj.save()
    print("Course " + course_name + ' saved in database')
    return obj
    #except:
    #print("Error in storing the Course object")
    #return None


def handle_teacher(teacher_name, teacher_name_ar, teacher_mobile):
    try:
        obj = Teacher.objects.get(teacher_name_ar=teacher_name_ar)
    except Teacher.DoesNotExist:
        obj = Teacher()
    obj.teacher_name_ar = teacher_name_ar
    obj.teacher_name = teacher_name
    obj.teacher_mobile = teacher_mobile
    try:
        obj.save()
        print("Teacher " + teacher_name_ar + ' saved in database')
        return obj
    except:
        print("Error in storing the Teacher object")
        return None


def handle_section(section_code, section_course):
    try:
        obj = Section.objects.get(section_code=section_code)
        print('Section found with id = ' + str(obj.section_id))
    except Section.DoesNotExist:
        obj = Section()
        print('Section not found, creating new object')
    obj.section_code = section_code
    obj.section_course = section_course

    try:
        obj.save()
        print("Section " + str(section_code) + ' saved in database')
        return obj
    except:
        print("Error in storing the Section object")
        return None


def handle_section_teachers(section_code, section_teacher):
    try:
        obj = Section.objects.get(section_code=section_code)
        print('Section found with id = ' + str(obj.section_id))
        obj.section_teachers.add(section_teacher)
        try:
            obj.save()
            print("Section " + str(section_code) + ' teacher list updated in database')
            return obj
        except:
            print("Error in updating teachers in the Section object")
            return None
    except Section.DoesNotExist:
        print('Section not found !!!*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')


def import_data(modeladmin, request, queryset):
    __file = 'ZARKA.xlsx'
    workbook = xl.open_workbook(__file, on_demand=True, encoding_override='UTF8')
    worksheet = workbook.sheet_by_index(0)

    ___line = 0
    _____location_ar = ''
    _____location_en = ''
    _____location_obj = None
    _____college_ar = ''
    _____college_en = ''
    _____college_obj = None
    _____department_ar = ''
    _____department_en = ''
    _____Department_obj = None
    _____course_ar = ''
    _____course_en = ''
    _____course_code = ''
    _____course_obj = None
    _____teacher = ''
    _____teacher__obj = None
    _____section = 0
    _____section_obj = None

    while True:

        try:
            tmp1 = worksheet.cell_value(___line, 2)
            tmp2 = worksheet.cell_value(___line, 1)
            tmp3 = worksheet.cell_value(___line, 3)

            if (tmp1 == 'المقر :'):
                _____location_ar = worksheet.cell_value(___line, 7)
                _____location_en = Translate(_____location_ar)
                _____location_obj = handle_location(_____location_ar, _____location_en)
            if (tmp1 == 'الكلية :'):
                _____college_ar = worksheet.cell_value(___line, 7)
                _____college_en = Translate(_____college_ar)
                _____college_obj = handle_college(_____college_en, _____college_ar, _____location_obj)
            if (tmp2 == 'القسم :'):
                _____department_ar = worksheet.cell_value(___line, 6)
                _____department_en = Translate(_____department_ar)
                _____Department_obj = handle_department(_____department_en, _____department_ar, _____college_obj)
            if (tmp3 == 'الشعبة'):
                ___line = ___line + 2
                __test = worksheet.cell_value(___line, 2)
                while (__test != 'المقر :'):
                    if worksheet.cell_value(___line, 12) != '':
                        _____course_ar = worksheet.cell_value(___line, 12)
                        _____course_code = worksheet.cell_value(___line, 9)
                        _____course_code = _____course_code[0:3] + '---' + _____course_code[3:]
                        _____course_en = Translate(_____course_ar)
                        _____course_obj = handle_course(_____course_code, _____course_en, _____course_ar,
                                                        _____Department_obj)

                        _____teacher = worksheet.cell_value(___line, 8)
                        _____teacher_name = _____teacher.split('-')[0]
                        _____teacher_phone = int(_____teacher.split('-')[1])
                        _____teacher__obj = handle_teacher('', _____teacher_name, _____teacher_phone)

                        _____section = int(worksheet.cell_value(___line, 3))
                        _____section_obj = handle_section(_____section, _____course_obj)
                        handle_section_teachers(_____section, _____teacher__obj)


                    else:
                        _____teacher = worksheet.cell_value(___line, 8)
                        _____teacher_name = _____teacher.split('-')[0]
                        _____teacher_phone = int(_____teacher.split('-')[1])
                        _____teacher__obj = handle_teacher('', _____teacher_name, _____teacher_phone)
                        handle_section_teachers(_____section, _____teacher__obj)

                    ___line = ___line + 1
                    __test = worksheet.cell_value(___line, 2)

                ___line = ___line - 1

            ___line = ___line + 1





        except IndexError:
            break


import_data.short_description = "Import data from excel sheet"


def import_data2(modeladmin, request, queryset):
    __file = 'ZARKA.xlsx'
    workbook = xl.open_workbook(__file, on_demand=True, encoding_override='UTF8')
    worksheet = workbook.sheet_by_index(0)

    _____data = {}

    ___line = 0
    _____location_ar = ''
    _____college_ar = ''
    _____department_ar = ''
    _____course_ar = ''
    _____course_code = ''
    _____teacher = ''
    _____section = 0

    import csv

    with open('data.csv', 'w') as csvfile:
        fieldnames = ['location', 'college', 'department', 'course_code', 'course_name', 'section', 'teacher_name',
                      'teacher_mobile']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quotechar='|')

        writer.writeheader()
        while True:

            try:
                tmp1 = worksheet.cell_value(___line, 2)
                tmp2 = worksheet.cell_value(___line, 1)
                tmp3 = worksheet.cell_value(___line, 3)

                if (tmp1 == 'المقر :'):
                    _____location_ar = worksheet.cell_value(___line, 7)
                if (tmp1 == 'الكلية :'):
                    _____college_ar = worksheet.cell_value(___line, 7)
                if (tmp2 == 'القسم :'):
                    _____department_ar = worksheet.cell_value(___line, 6)
                if (tmp3 == 'الشعبة'):
                    ___line = ___line + 2
                    __test = worksheet.cell_value(___line, 2)
                    while (__test != 'المقر :'):
                        ____course_test = worksheet.cell_value(___line, 12)
                        if ____course_test != '':
                            _____course_ar = worksheet.cell_value(___line, 12)
                            _____course_code = worksheet.cell_value(___line, 9)
                            _____teacher = worksheet.cell_value(___line, 8)
                            _____section = int(worksheet.cell_value(___line, 3))
                            _____teacher_name = _____teacher.split('-')[0]
                            _____teacher_phone = int(_____teacher.split('-')[1])
                            writer.writerow({'location': _____location_ar, 'college': _____college_ar,
                                             'department': _____department_ar, 'course_code': _____course_code,
                                             'course_name': _____course_ar, 'section': _____section,
                                             'teacher_name': _____teacher_name, 'teacher_mobile': _____teacher_phone})


                        else:
                            _____teacher = worksheet.cell_value(___line, 8)
                            _____teacher_name = _____teacher.split('-')[0]
                            _____teacher_phone = int(_____teacher.split('-')[1])

                            writer.writerow({'location': _____location_ar, 'college': _____college_ar,
                                             'department': _____department_ar, 'course_code': _____course_code,
                                             'course_name': _____course_ar, 'section': _____section,
                                             'teacher_name': _____teacher_name, 'teacher_mobile': _____teacher_phone})

                        ___line = ___line + 1
                        __test = worksheet.cell_value(___line, 2)

                    ___line = ___line - 1

                ___line = ___line + 1





            except IndexError:
                break
import_data2.short_description = "Import data from excel sheet 2"


def apply_translation(modeladmin, request, queryset):

    for _location in Location.objects.all():
        if _location.location_name_ar is None:
            continue
        _location.location_name = Translate(_location.location_name_ar)
        _location.save()

    for _college in College.objects.all():
        if _college.college_name_ar is None:
            continue
        _college.college_name = Translate(_college.college_name_ar)
        _college.save()

    for _department in Department.objects.all():
        if _department.department_name_ar is None:
            continue
        _department.department_name = Translate(_department.department_name_ar)
        _department.save()

    for _course in Course.objects.all():
        if _course.course_name_ar is None:
            continue
        _course.course_name = Translate(_course.course_name_ar)
        _course.save()

    print('Translation process done')
    messages(request, "Translation process done", level=messages.ERROR)

apply_translation.short_description = "Apply Translation to all the Data"

def generate_translation_list(modeladmin, request, queryset):
    import docx

    _translation_list = Translation.objects.all()

    document = docx.Document()

    document.add_heading('Translation List', 0)

    p = document.add_paragraph('A plain paragraph having some ')
    p.add_run('bold').bold = True
    p.add_run(' and some ')
    p.add_run('italic.').italic = True

    document.add_heading('Heading, level 1', level=1)
    document.add_paragraph('Intense quote', style='Intense Quote')

    document.add_paragraph(
        'first item in unordered list', style='List Bullet'
    )
    document.add_paragraph(
        'first item in ordered list', style='List Number'
    )

    #document.add_picture('monty-truth.png', width=docx.shared.Inches(1.25))

    records = (
        (3, '101', 'Spam'),
        (7, '422', 'Eggs'),
        (4, '631', 'Spam, spam, eggs, and spam')
    )

    table = document.add_table(rows=1, cols=3)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Arabic'
    hdr_cells[1].text = 'English'
    hdr_cells[2].text = 'Remarks'
    for _translation in _translation_list:
        _translation
        row_cells = table.add_row().cells
        row_cells[0].text = _translation.translation_ar
        row_cells[1].text = _translation.translation_en
        row_cells[2].text = ''

    #document.add_page_break()

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=download.docx'
    document.save(response)
    return response

generate_translation_list.short_description = "Genrate Translation Report"



#################################################################################
def export_as_csv(modeladmin, request, queryset):
    field_names = ['ARABIC', 'ENGLISH']

    with open('data/translations/translations.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names, delimiter=';')
        writer.writeheader()
        for obj in Translation.objects.all():
            writer.writerow({'ARABIC': obj.translation_ar, 'ENGLISH': obj.translation_en})


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=translations.csv'
    writer = csv.DictWriter(response, fieldnames=field_names, delimiter=';')
    writer.writeheader()
    for _obj in Translation.objects.all():
        writer.writerow({'ARABIC': _obj.translation_ar, 'ENGLISH': _obj.translation_en})

    return response
export_as_csv.short_description = "Export Translations to CSV"


#################################################################################
def import_from_csv(modeladmin, request, queryset):
    with open('data/translations/translations.csv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            _ar = row['ARABIC']
            _en = row['ENGLISH']

            try:
                obj = Translation.objects.get(translation_ar=_ar)
                obj.translation_en = _en
                obj.save()
            except Translation.DoesNotExist:
                obj = Translation()
                obj.translation_ar = _ar
                obj.translation_en = _en
                obj.save()

import_from_csv.short_description = "Import Translations from CSV"




class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'location_id', 'location_name_ar', 'location_name')
    actions = [import_data, import_data2]


class CollegeAdmin(admin.ModelAdmin):
    list_display = (
        'college_id', 'college_name', 'college_location')
    search_fields = ('college_name', 'college_location__location_name')
    list_filter = ('college_location',)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        'department_id', 'department_name', 'department_location')
    search_fields = ('department_name', 'department_location')
    list_filter = ('department_location__college_location__location_name', 'department_location__college_name')


class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'course_id', 'course_code', 'course_name', 'course_name_ar', 'course_department')
    search_fields = ('course_code', 'course_name', 'course_name_ar')
    list_filter = (
        'course_department__department_name', 'course_department__department_location__college_name',
        'course_department__department_location__college_location__location_name')


class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'teacher_id', 'teacher_name', 'teacher_name_ar', 'teacher_mobile')
    search_fields = ('teacher_name', 'teacher_name_ar', 'teacher_mobile')


class SectionAdmin(admin.ModelAdmin):
    list_display = (
        'section_code', 'section_course',)
    search_fields = ('section_code',)


class SectionDocRequestAdmin(admin.ModelAdmin):
    list_display = (
       'section', 'created_date')
    list_filter = ('created_date',)

class CourseDocRequestAdmin(admin.ModelAdmin):
    list_display = (
       'course', 'created_date')
    list_filter = ('created_date',)


class TranslationAdmin(admin.ModelAdmin):
    list_display = (
        'translation_ar', 'translation_en')
    actions = [generate_translation_list, apply_translation, export_as_csv, import_from_csv]


admin.site.register(Location, LocationAdmin)
admin.site.register(College, CollegeAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Section, SectionAdmin)

admin.site.register(Translation, TranslationAdmin)

admin.site.register(SectionDocRequest, SectionDocRequestAdmin)
admin.site.register(CourseDocRequest, CourseDocRequestAdmin)
