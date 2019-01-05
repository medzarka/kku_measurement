from django.contrib import admin

from .models import UploadDocument
from .models import GeneratedDocument
from .models import Translation

from measurement.models import SectionDocRequest
from measurement.models import CourseDocRequest

from periods.models import Semester
from HR.models import Teacher
from departments.models import Location
from departments.models import College
from departments.models import Department
from departments.models import Section

from courses.models import Speciality
from courses.models import Course
from courses.models import AcademicLevel
from django.core.files import File

import xlrd as xl
from googletrans import Translator
import csv
from django.http import HttpResponse
import os
import statistics
import matplotlib
from django.shortcuts import render
from matplotlib import pyplot as plt
from scipy.stats import pearsonr
from scipy.stats import skew
from django.utils.datastructures import MultiValueDictKeyError
from scipy.stats import norm
import numpy as np
import scipy
from threading import BoundedSemaphore
max_items = 1
sem = BoundedSemaphore(max_items)


def Translate(translation_ar):
    try:
        obj = Translation.objects.get(translation_ar=translation_ar)
        # print('Translation found with id = ' + str(obj.translation_id))
        return obj.translation_en

    except Translation.DoesNotExist:
        obj = Translation()
        # print('Translation not found, creating new object')
        translator = Translator(service_urls=['translate.google.com.sa', 'translate.google.com'])
        translation_en = translator.translate(translation_ar, dest='en').text
        obj.translation_ar = translation_ar
        obj.translation_en = translation_en
        try:
            obj.save()
            # print("Translation for " + translation_ar + ' saved in database')
            return obj.translation_en
        except Exception as e:
            print("Error in storing the Translation object")
            print(str(e))
            return None


def handle_location(_____location_ar, _____location_en):
    try:
        obj = Location.objects.get(location_name=_____location_en)
        # print('Location found with id = ' + str(obj.location_id))
    except Location.DoesNotExist:
        obj = Location()
        # print('Location not found, creating new object')
    obj.location_name = _____location_en
    obj.location_name_ar = _____location_ar

    try:
        obj.save()
        print("Location " + _____location_en + ' saved in database')
        return obj
    except Exception as e:
        print("Error in storing the Location object")
        print(str(e))
        return None


def handle_college(college_name, college_name_ar, college_location):
    try:
        obj = College.objects.get(college_name=college_name)
        # print('College found with id = ' + str(obj.college_id))
    except College.DoesNotExist:
        obj = College()
        # print('College not found, creating new object')
    obj.college_name = college_name
    obj.college_name_ar = college_name_ar
    obj.college_location = college_location

    try:
        obj.save()
        # print("College " + college_name + ' saved in database')
        return obj
    except Exception as e:
        print("Error in storing the College object")
        print(str(e))
        return None


def handle_department(department_name, department_name_ar, department_location):
    try:
        obj = Department.objects.get(department_name=department_name)
        # print('Department found with id = ' + str(obj.department_id))
    except Department.DoesNotExist:
        obj = Department()
        # print('College not found, creating new object')
    obj.department_name = department_name
    obj.department_name_ar = department_name_ar
    obj.department_location = department_location

    try:
        obj.save()
        # print("Department " + department_name + ' saved in database')
        return obj
    except Exception as e:
        print("Error in storing the Department object")
        print(str(e))
        return None


def handle_speciality(speciality_name, speciality_name_ar):
    try:
        obj = Speciality.objects.get(speciality_name=speciality_name)
        # print('Department found with id = ' + str(obj.department_id))
    except Speciality.DoesNotExist:
        obj = Speciality()
        # print('College not found, creating new object')
    obj.speciality_name = speciality_name
    obj.speciality_name_ar = speciality_name_ar

    try:
        obj.save()
        # print("Department " + department_name + ' saved in database')
        return obj
    except Exception as e:
        print("Error in storing the Speciality object")
        print(str(e))
        return None


def handle_course(course_code, course_name, course_name_ar, course_speciality, academic_level):
    try:
        obj = Course.objects.get(course_code=course_code)
        print('Course found with id = ' + str(obj.course_id))
    except Course.DoesNotExist:
        obj = Course()
        print('Course not found, creating new object')
    obj.course_name = course_name
    obj.course_code = course_code
    obj.course_name_ar = course_name_ar
    obj.speciality = course_speciality
    obj.academic_level = academic_level

    try:
        obj.save()
        print("Course " + course_name + ' saved in database')
        return obj
    except Exception as e:
        print("Error in storing the Course object")
        print(str(e))
        return None


def handle_teacher(teacher_name, teacher_name_ar, teacher_mobile):
    try:
        obj = Teacher.objects.get(teacher_name_ar=teacher_name_ar)
    except Teacher.DoesNotExist:
        obj = Teacher()
    obj.teacher_name_ar = teacher_name_ar
    obj.teacher_name = teacher_name
    obj.teacher_mobile = teacher_mobile

    obj.save()
    print("Teacher " + teacher_name_ar + ' saved in database')
    return obj


def handle_section(section_code, section_course, section_department, section_semester):
    try:
        obj = Section.objects.get(section_code=section_code)
        print('Section found with id = ' + str(obj.section_id))
    except Section.DoesNotExist:
        obj = Section()
        print('Section not found, creating new object')
    obj.section_code = section_code
    obj.section_course = section_course
    obj.section_department = section_department
    obj.section_semester = section_semester

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
    for doc in queryset:
        print('Hanlding file ' + doc.upload_document_document.url)

        # __file = 'ZARKA.xlsx'
        __file = doc.upload_document_document.url
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
        _____Speciality_obj = None
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

                semester__obj = Semester.objects.filter(semester_isInUse=True)[0]
                level__obj = AcademicLevel.objects.filter(academic_level_name='L1')[0]

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
                    _____Speciality_obj = handle_speciality(_____department_en, _____department_ar)
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
                                                            _____Speciality_obj, level__obj)

                            _____teacher = worksheet.cell_value(___line, 8)
                            _____teacher_name = _____teacher.split('-')[0]
                            _____teacher_phone = int(_____teacher.split('-')[1])
                            _____teacher__obj = handle_teacher('', _____teacher_name, _____teacher_phone)

                            _____section = int(worksheet.cell_value(___line, 3))
                            _____section_obj = handle_section(_____section, _____course_obj, _____Department_obj,
                                                              semester__obj)
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
import_data.short_description = "Import Course/Departments/Sections from excel sheet"


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


apply_translation.short_description = "Apply Translation to all the Data"


#################################################################################
def export_translation(modeladmin, request, queryset):
    field_names = ['ARABIC', 'ENGLISH']

    import uuid
    __filename = str(uuid.uuid4())
    with open(__filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names, delimiter=';')
        writer.writeheader()
        for obj in Translation.objects.all():
            writer.writerow({'ARABIC': obj.translation_ar, 'ENGLISH': obj.translation_en})

    django_file = File(open(__filename, 'rb'))

    __obj = GeneratedDocument()
    __obj.generated_document_description = "Generated Document for Translation"
    __obj.generated_document_document.save("generated_translations.csv", django_file, save=True)
    __obj.save()

    os.remove(__filename)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=translations.csv'
    writer = csv.DictWriter(response, fieldnames=field_names, delimiter=';')
    writer.writeheader()
    for _obj in Translation.objects.all():
        writer.writerow({'ARABIC': _obj.translation_ar, 'ENGLISH': _obj.translation_en})

    return response


export_translation.short_description = "Export Translations to a csv file"


#################################################################################
def import_Translation(modeladmin, request, queryset):
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


import_Translation.short_description = "Import Translations from CSV"



def section_action(modeladmin, request, queryset):
    import fnmatch
    import os
    import os.path
    import re

    includes = ['*.xls']  # for files only

    # transform glob patterns to regular expressions
    includes = r'|'.join([fnmatch.translate(x) for x in includes])

    for root, dirs, files in os.walk('data/media/documents/upload/'):

        # exclude dirs
        dirs[:] = [os.path.join(root, d) for d in dirs]

        # exclude/include files
        files = [os.path.join(root, f) for f in files]
        files = [f for f in files if re.match(includes, f)]

        for fname in files:
            print(fname.__str__())

    for doc in files:
        print('Hanlding file ' + doc.__str__())

        __file = doc.__str__()
        __analysis = []
        context = {}
        __grades = ''
        __domain = request.get_host()

        __location = ''
        __teachers = ''
        __college = ''
        __department = ''
        __course = ''
        __course_code = ''
        __section = ''
        __message = ''
        __mean = 0
        __std = 0
        __min = 0
        __max = 0
        __skewness = 0
        __correlation = 0
        __show__result = 0
        __histogramfile = ''

        __mids = []
        __finals = []
        __totals = []
        __line = 7

        try:
            __grades = __file
            sem.acquire()
            print("The semaphore is locked")



            # upload the file
            _grades_uploaded_file = __grades

            # read the content of the uploaded file
            workbook = xl.open_workbook(_grades_uploaded_file, on_demand=True)
            worksheet = workbook.sheet_by_index(0)
            try:
                ____tmp = worksheet.cell_value(6, 5)
            except IndexError:
                ____tmp = ''

            __section = int(worksheet.cell_value(4, 1))
            __location = worksheet.cell_value(0, 1)

            if __section == '':
                raise Exception('Unable to read the section from the excel file !!!')
            if __location == '':
                raise Exception('Unable to read the location from the excel file !!!')

            __section_obj = None
            __actualSemester = Semester.objects.get(semester_isInUse=True)
            for _mytest in Section.objects.all():
                if _mytest.section_department.department_location.college_location.location_name_ar == __location \
                        and _mytest.section_code == __section\
                        and _mytest.section_semester == __actualSemester:
                    __section_obj = _mytest
                    print('Section found with id = ' + str(_mytest.section_id))
                    __location = _mytest.section_department.department_location.college_location.location_name
                    __college = _mytest.section_department.department_location.college_name
                    __department =_mytest.section_department.department_name
                    __course = _mytest.section_course.course_name
                    __course_code = _mytest.section_course.course_code
                    for _teach in _mytest.section_teachers.all():
                        __teachers = __teachers + ' ' + _teach.teacher_name_ar
                    break

            if ____tmp == '':  # grades without mids
                while True:
                    try:
                        __student = worksheet.cell_value(__line, 0)
                        if worksheet.cell_value(__line, 2) != '':
                            __finals.append(int(worksheet.cell_value(__line, 2)))
                        if worksheet.cell_value(__line, 3) != '':
                            __totals.append(int(worksheet.cell_value(__line, 3)))
                        __line += 1
                    except IndexError:
                        break
            else:
                while True:
                    try:
                        __student = worksheet.cell_value(__line, 0)
                        if worksheet.cell_value(__line, 2) != '':
                            __mids.append(int(worksheet.cell_value(__line, 2)))
                        if worksheet.cell_value(__line, 3) != '':
                            __finals.append(int(worksheet.cell_value(__line, 3)))
                        if worksheet.cell_value(__line, 4) != '':
                            __totals.append(int(worksheet.cell_value(__line, 4)))
                        __line += 1
                    except IndexError:
                        break

            # debug data

            # print('grades = ' + str(__grades))
            # print('Section = ' + str(__section))
            # print('MIDs = ' + str(__mids))
            # print('Finals = ' + str(__finals))
            # print('Totals = ' + str(__totals))

            # compute statistics about the course grades

            if __section_obj == None:
                raise Exception('Unable to recognise the section in the database !!!')

            if __section != '' and __section_obj != None:
                __message = 'The grade Excel file was well loaded'
                __mean = float("{0:.4f}".format(statistics.mean(__totals)))
                __std = float("{0:.4f}".format(statistics.stdev(__totals)))
                __skewness = float("{0:.4f}".format(skew(__totals, bias=False)))
                if len(__mids) == 0:
                    __correlation = -99.99
                else:
                    __correlation = float("{0:.4f}".format(pearsonr(__mids, __finals)[1]))
                __min = min(__totals)
                __max = max(__totals)

                # plot the histogram

                a = np.array(__totals)
                # Fit a normal distribution to the data:
                mu, std = norm.fit(a)
                number = a.size

                # Plot the histogram.
                plt.hist(a, bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], density=True, color='#607c8e',
                         edgecolor='black',
                         rwidth=0.8)
                # Plot the PDF.
                x = np.linspace(0, 100, 100)
                p = norm.pdf(x, mu, std)
                plt.plot(x, p, 'k', linewidth=3)
                title = "Histogram: Section = %d,  Number of Students = %d" % (__section, number)
                plt.title(title)

                __histogramfile = "data/media/histogram_section" + str(__section) + ".png"
                plt.savefig(__histogramfile)
                plt.close()

                print("mean : " + str(__mean))
                print("std : " + str(__std))
                print("skewness : " + str(__skewness))
                print("correlation : " + str(__correlation))

                __show__result = 1
                # save the section analysis
                __grades_data = {}
                __grades_data['mids'] = __mids
                __grades_data['finals'] = __finals
                __grades_data['totals'] = __totals
                str_grades = str(__grades_data)  # inverse dict2 = eval(str1)

                try:
                    obj = SectionDocRequest.objects.get(section=__section_obj)
                    print("--------> Updating the section data with id= " + str(obj.section_doc_id))
                except SectionDocRequest.DoesNotExist:
                    obj = SectionDocRequest()
                    print("--------> Creating new section data")

                obj.doc_correlation = __correlation
                obj.doc_explanation = ''
                obj.doc_max = __max
                obj.doc_mean = __mean
                obj.doc_min = __min
                obj.doc_skewness = __skewness
                obj.doc_std_deviation = __std
                obj.histogram = __histogramfile
                obj.student_grades = str_grades
                obj.section = __section_obj

                obj.save()


        except MultiValueDictKeyError:
            __message = 'Please fill all the form.'
        except ValueError as e:
            __message = 'Please use the grade file provided by the registration portal (Academia) without any change.'
            print(str(e))

        finally:
            sem.release()
            print("The semaphore was released")

    print('######################################################')
    print('######################################################')

    __courses_list = Course.objects.all()
    for a_course in __courses_list:
        __course_id = a_course.course_code
        __course_obj = None
        __section_objects = []
        __sections = []
        __message = ''
        __mean = 0
        __std = 0
        __min = 0
        __max = 0
        __skewness = 0
        __ttest_annova_type = ''
        __ttest_annova_value = 0
        __ttest_annova_sig = 0
        __correlation = 0
        __show__result = 0
        __histogramfile = ''
        __mids = []
        __finals = []
        __totals = []
        __domain = ''
        __course = ''
        counter = 0
        __nbr_sections = 0
        __found_section = 0
        try:
            sem.acquire()

            __course_obj = a_course

            __course = __course_obj.course_name_ar

            for _section in Section.objects.all():
                if _section.section_course == __course_obj:
                    __section_objects.append(_section)
                    __nbr_sections += 1
            #print('Dealing with  ' + str(__nbr_sections) + ' sections : ' + str(__section_objects))
            if __nbr_sections < 2:
                raise Exception('course '+ str(_section.section_code) +' ignored')

            for _section in __section_objects:
                for _report in SectionDocRequest.objects.all():
                    if _report.section.section_code == _section.section_code:
                        __sections.append(_report)
                        __found_section += 1
                        __data = eval(_report.student_grades)
                        for grade in __data['mids']:
                            __mids.append(grade)
                        for grade in __data['finals']:
                            __finals.append(grade)
                        for grade in __data['totals']:
                            __totals.append(grade)
                        break
            #print('Dealing with  ' + str(__found_section) + ' section reports: ' + str(__sections))

            if __nbr_sections != __found_section:
                raise Exception(' -->  Some sections need to be analysed first')

            print('---------------------------------------------------')
            print('Dealing with course ' + __course_obj.course_name_ar)

            # compute statistics about the course grades
            __mean = float("{0:.4f}".format(statistics.mean(__totals)))
            __std = float("{0:.4f}".format(statistics.stdev(__totals)))
            __skewness = float("{0:.4f}".format(skew(__totals, bias=False)))
            if len(__mids) == 0:
                __correlation = -99.99
            else:
                __correlation = float("{0:.4f}".format(pearsonr(__mids, __finals)[1]))
            __min = min(__totals)
            __max = max(__totals)
            print('Dealing with ' + str(__nbr_sections) + ' sections.')

            if __nbr_sections == 2:
                # T-Test
                __ttest_annova_type = 'T-Test'
                _total1 = eval(__sections[0].student_grades)['totals']
                _total2 = eval(__sections[1].student_grades)['totals']
                res = scipy.stats.ttest_ind(_total1, _total2)

                __ttest_annova_value = float("{0:.4f}".format(res.statistic))
                __ttest_annova_sig = float("{0:.4f}".format(res.pvalue))

            else:
                # annova
                __ttest_annova_type = 'ANOVA'
                if len(__sections) == 3:
                    __ttest_annova_value = float("{0:.4f}".format(
                        scipy.stats.f_oneway(eval(__sections[0].student_grades)['totals'],
                                             eval(__sections[1].student_grades)['totals'],
                                             eval(__sections[2].student_grades)['totals'])[0]))
                    __ttest_annova_sig = float("{0:.4f}".format(
                        scipy.stats.f_oneway(eval(__sections[0].student_grades)['totals'],
                                             eval(__sections[1].student_grades)['totals'],
                                             eval(__sections[2].student_grades)['totals'])[1]))
                elif len(__sections) == 4:
                    __ttest_annova_value = float("{0:.4f}".format(
                        scipy.stats.f_oneway(eval(__sections[0].student_grades)['totals'],
                                             eval(__sections[1].student_grades)['totals'],
                                             eval(__sections[2].student_grades)['totals'],
                                             eval(__sections[3].student_grades)['totals'])[0]))
                    __ttest_annova_sig = float("{0:.4f}".format(
                        scipy.stats.f_oneway(eval(__sections[0].student_grades)['totals'],
                                             eval(__sections[1].student_grades)['totals'],
                                             eval(__sections[2].student_grades)['totals'],
                                             eval(__sections[3].student_grades)['totals'])[1]))
                elif len(__sections) == 5:
                    __ttest_annova_value = float("{0:.4f}".format(
                        scipy.stats.f_oneway(eval(__sections[0].student_grades)['totals'],
                                             eval(__sections[1].student_grades)['totals'],
                                             eval(__sections[2].student_grades)['totals'],
                                             eval(__sections[3].student_grades)['totals'],
                                             eval(__sections[4].student_grades)['totals'])[0]))
                    __ttest_annova_sig = float("{0:.4f}".format(
                        scipy.stats.f_oneway(eval(__sections[0].student_grades)['totals'],
                                             eval(__sections[1].student_grades)['totals'],
                                             eval(__sections[2].student_grades)['totals'],
                                             eval(__sections[3].student_grades)['totals'],
                                             eval(__sections[4].student_grades)['totals'])[1]))
                else:
                    raise Exception('To be implemented : managing more that 5 sections per a course !!!!')

            print("mean : " + str(__mean))
            print("std : " + str(__std))
            print("skewness : " + str(__skewness))
            print("__ttest_annova_type : " + str(__ttest_annova_type))
            print("__ttest_annova_value : " + str(__ttest_annova_value))
            print("__ttest_annova_sig : " + str(__ttest_annova_sig))

            # plot the histogram

            a = np.array(__totals)
            # Fit a normal distribution to the data:
            mu, std = norm.fit(a)
            number = a.size

            # Plot the histogram.
            plt.hist(a, bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], density=True, color='#607c8e',
                     edgecolor='black',
                     rwidth=0.8)
            # Plot the PDF.
            x = np.linspace(0, 100, 100)
            p = norm.pdf(x, mu, std)
            plt.plot(x, p, 'k', linewidth=3)
            title = "Histogram for course: " + __course_obj.course_name + ",  N=%d" % (number)
            plt.title(title)

            __histogramfile = "data/media/histogram_course_" + str(__course) + ".png"
            plt.savefig(__histogramfile)
            plt.close()

            print("mean : " + str(__mean))
            print("std : " + str(__std))
            print("skewness : " + str(__skewness))
            print("correlation : " + str(__correlation))

            __show__result = 1

            try:
                obj = CourseDocRequest.objects.get(course=__course_obj)
                print("--------> Updating the course report data with id= " + str(obj.course_doc_id))
            except CourseDocRequest.DoesNotExist:
                obj = CourseDocRequest()
                obj.course = __course_obj
                print("--------> Creating new course report data")

            obj.doc_correlation = __correlation
            obj.doc_explanation = ''
            obj.doc_max = __max
            obj.doc_mean = __mean
            obj.doc_min = __min
            obj.doc_skewness = __skewness
            obj.doc_std_deviation = __std
            obj.histogram = __histogramfile
            obj.doc_ttest_annova_sig = __ttest_annova_sig
            obj.doc_ttest_annova_value = __ttest_annova_value
            obj.doc_ttest_annova_type = __ttest_annova_type

            obj.save()
            print("Course Report saved with id = " + str(obj.course_doc_id))

        except Exception as e:
            __message = e.__str__()

        finally:
            sem.release()
            print(__message)
section_action.short_description = "Import Section Grades"


def section_docx(request):
    __section_obj = None
    __section_report_obj = None
    __section_id = 0
    context = {}

    return render(request, 'section.html', context=context)



class UploadDocumentAdmin(admin.ModelAdmin):
    list_display = (
        'upload_document_id', 'upload_document_document', 'upload_document_description', 'upload_document_uploaded_at')
    actions = [import_data, import_Translation, section_action]


class GeneratedDocumentAdmin(admin.ModelAdmin):
    list_display = (
        'generated_document_id', 'generated_document_document', 'generated_document_description',
        'generated_document_generated_at')


class TranslationAdmin(admin.ModelAdmin):
    list_display = (
        'translation_ar', 'translation_en')
    actions = [export_translation]


admin.site.register(UploadDocument, UploadDocumentAdmin)
admin.site.register(GeneratedDocument, GeneratedDocumentAdmin)
admin.site.register(Translation, TranslationAdmin)
