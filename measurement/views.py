# -*- coding: utf-8 -*-

import os
import statistics

import matplotlib
import xlrd as xl
from django.shortcuts import render
from matplotlib import pyplot as plt
from scipy.stats import pearsonr
from scipy.stats import skew
from .models import SectionDocRequest
from .models import CourseDocRequest
from django.utils.datastructures import MultiValueDictKeyError
import time
from scipy.stats import norm
import numpy as np
from threading import BoundedSemaphore
from .models import Course
from .models import Section
import scipy
import docx
from django.http import HttpResponse

matplotlib.use('Agg')

max_items = 1
sem = BoundedSemaphore(max_items)


def index(request):
    context = {}
    return render(request, 'index.html', context=context)


def section(request):
    context = {
    }
    return render(request, 'section.html', context=context)


def analysis(context):
    __analysis = []
    _mean = context['mean']
    if _mean > 90:
        __analysis.append('The Grades Mean is High')
    if _mean < 60:
        __analysis.append('The Grades Mean is Low')
    if 60 <= _mean <= 90:
        __analysis.append('The Grades Mean is Normal')

    _std = context['std']
    if _std < 5:
        __analysis.append('The spread of grades is Low --> the grades are very close')
    if _std > 15:
        __analysis.append('The spread of grades is  High --> the grades are very far')
    if 15 > _std > 5:
        __analysis.append('The spread of grades is  correct')

    _skewness = context['skewness']
    if _skewness >= 0:
        __analysis.append('The skewness of positive --> Most of grades are less than the mean.')
    else:
        __analysis.append('The skewness of negative --> Most of grades are more than the mean.')

    _correlation = context['correlation']
    if _correlation >= 0.05:
        __analysis.append(
            'The correlation is greater or equal to 0.05 --> There is no correlation between Mids and Finals.')
    else:
        __analysis.append('The correlation is less than 0.05 --> There is a good correlation between Mids and Finals.')

    try :
        _ttest_annova_sig = context['ttest_annova_sig']
        if _ttest_annova_sig >= 0.05:
            __analysis.append(
                'The section results are very close.')
        else:
            __analysis.append('There are difference in section results.')
    except :
        pass

    return __analysis


def course(request):
    context = {}
    __courses = {}
    __courses_names = {}

    __courses_handling = []

    for _course in Course.objects.all():
        __courses_names[_course.course_code] = _course

    for _section in Section.objects.all():
        try:
            __courses[_section.section_course.course_code] = __courses[_section.section_course.course_code] + 1
        except:
            __courses[_section.section_course.course_code] = 1

    for key in __courses.keys():
        if __courses[key] > 1:
            __courses_handling.append(__courses_names[key])

    context = {
        'courses': __courses_handling,
    }
    return render(request, 'course.html', context=context)


def department(request):
    context = {}
    return render(request, 'department.html', context=context)


def section_action(request):
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
        sem.acquire()
        print("The semaphore is locked")
        __grades = request.FILES['grades']

        if request.method == 'GET':
            raise Exception('Internal Error')

        if request.method == 'POST':

            # upload the file
            _grades_uploaded_file = 'data/upload/' + str(__grades)
            if not os.path.exists('data/upload/'):
                os.mkdirs('data/upload/')

            with open(_grades_uploaded_file, 'wb+') as destination:
                for chunk in __grades.chunks():
                    destination.write(chunk)

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

            __newfilename = 'data/upload/section_' + str(__section) + _grades_uploaded_file[-4:]
            os.rename(_grades_uploaded_file, __newfilename)

            __section_obj = None
            for _mytest in Section.objects.all():
                if _mytest.section_course.course_department.department_location.college_location.location_name_ar == __location \
                        and _mytest.section_code == __section:
                    __section_obj = _mytest
                    print('Section found with id = ' + str(_mytest.section_id))
                    __location = _mytest.section_course.course_department.department_location.college_location.location_name
                    __college = _mytest.section_course.course_department.department_location.college_name
                    __department = _mytest.section_course.course_department.department_name
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

                # get the server domain
                if request.is_secure():
                    __domain = 'https://' + request.get_host()
                else:
                    __domain = 'http://' + request.get_host()
                __security = request.is_secure()



    except MultiValueDictKeyError:
        __message = 'Please fill all the form.'
    except ValueError as e:
        __message = 'Please use the grade file provided by the registration portal (Academia) without any change.'
        print(str(e))

    finally:
        sem.release()
        print("The semaphore was released")

    if len(__mids) == 0:
        __correlation = 'N/A'


    context = {
        'show_result': __show__result,
        'message': __message,
        'mean': __mean,
        'std': __std,
        'skewness': __skewness,
        'correlation': __correlation,
        'min': __min,
        'max': __max,
        'histogram': __histogramfile,
        'domain': __domain,
        'section': __section,
        'location': __location,
        'college': __college,
        'department': __department,
        'course': __course,
        'course_code': __course_code,
        'teachers': __teachers,
    }
    __results = analysis(context)
    context['analysis'] = __results



    del __grades
    del __section
    del __message
    del __mean
    del __std
    del __min
    del __max
    del __skewness
    del __correlation
    del __show__result
    del __histogramfile
    del __domain

    return render(request, 'section_result.html', context=context)


def section_docx(request):
    __section_obj = None
    __section_report_obj = None
    __section_id = 0
    context = {}

    return render(request, 'section.html', context=context)


def course_action(request):
    context = {}

    __course_id = int(request.POST['course'])
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
        print("The semaphore is locked")

        if request.method == 'GET':
            raise Exception('Internal Error')

        if request.method == 'POST':
            __course_obj = Course.objects.get(course_id=__course_id)
            print('Dealing with course ' + __course_obj.course_name_ar)
            __course = __course_obj.course_name_ar

            for _section in Section.objects.all():
                if _section.section_course.course_id == __course_id:
                    __section_objects.append(_section)
                    __nbr_sections += 1
            print('Dealing with  ' + str(__nbr_sections) + ' sections : ' + str(__section_objects))

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
            print('Dealing with  ' + str(__found_section) + ' section reports: ' + str(__sections))

            if __nbr_sections != __found_section:
                raise Exception('Some sections need to be analysed first')

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

            # get the server domain
            if request.is_secure():
                __domain = 'https://' + request.get_host()
            else:
                __domain = 'http://' + request.get_host()
            __security = request.is_secure()



    except Exception as e:
        __message = e.__str__()

    finally:
        sem.release()
        print("The semaphore was released")

    if len(__mids) == 0:
        __correlation = 'N/A'

    context = {
        'ttest_annova_sig': __ttest_annova_sig,
        'ttest_annova_type': __ttest_annova_type,
        'ttest_annova_value': __ttest_annova_value,
        'show_result': __show__result,
        'message': __message,
        'mean': __mean,
        'std': __std,
        'skewness': __skewness,
        'correlation': __correlation,
        'min': __min,
        'max': __max,
        'histogram': __histogramfile,
        'domain': __domain,
        'course': __course,
        'sections': __sections,
    }

    __results = analysis(context)
    context['analysis'] = __results

    del __course
    del __message
    del __mean
    del __std
    del __min
    del __max
    del __skewness
    del __correlation
    del __show__result
    del __histogramfile
    del __domain
    del __sections

    return render(request, 'course_result.html', context=context)


def department_action(request):
    context = {}
    return render(request, 'course.html', context=context)


def index2(request):
    pass
    """View function for home page of site.

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.    
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)"""


def anova(data):
    """
    return True is at least one mean is different from the other
https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.f_oneway.html
    """
    if len(data) == 2:
        statistic, pvalue = statistics.f_oneway(data[0], data[1])
    elif len(data) == 3:
        statistic, pvalue = statistics.f_oneway(data[0], data[1], data[2])
    elif len(data) == 4:
        statistic, pvalue = statistics.f_oneway(data[0], data[1], data[2], data[3])
    else:
        print("TODO ANOVA manage more values")
    print("ANOVA Statistic " + str(statistic) + " and p-value " + str(pvalue))
    if pvalue < 0.05:
        return True
    else:
        return False


def t_test(covariates, groups):
    """
    Two sample t test for the distribution of treatment and control covariates

    Parameters
    ----------
    covariates : DataFrame
        Dataframe with one covariate per column.
        If matches are with replacement, then duplicates should be
        included as additional rows.
    groups : array-like
        treatment assignments, must be 2 groups

    Returns
    -------
    A list of p-values, one for each column in covariates
    """
    colnames = list(covariates.columns)
    J = len(colnames)
    pvalues = np.zeros(J)
    for j in range(J):
        var = covariates[colnames[j]]
        res = statistics.ttest_ind(var[groups == 1], var[groups == 0])
        pvalues[j] = res.pvalue
    return pvalues
