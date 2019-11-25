import csv
import os
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.utils import timezone
from ..models import *


def index(request):                 #fix by vinayaka
    if request.user.is_authenticated:
        user = get_username(request)
        if user == 'admin':
            tcourses = Course.objects.all()
            scourses = []
            is_admin = 1
            return render(request, 'course/index.html', {'tcourses': tcourses, 'scourses': scourses, 'is_admin': is_admin})

        uobject = User.objects.all().filter(name=user)
        tcourses = []
        scourses = []
        if len(uobject) > 0:
            tcourses = uobject[0].course_teacher.all()
            scourses = uobject[0].course_student.all()
        is_admin = 0
        return render(request, 'course/index.html', {'tcourses': tcourses, 'scourses': scourses, 'is_admin': is_admin})
    else:
        return redirect('account/login')


def course_page(request, course):       #fix by vinayaka
    user = get_username(request)
    if not course_verify(course, user):
        return render(request, 'course/error.html')
    courseo = Course.objects.all().filter(title=course)[0]
    is_teacher = 0
    if user == 'admin':
        is_teacher = 1
    else:
        uobj = User.objects.all().filter(name=user)[0]
        if uobj in courseo.teachers.all():
            is_teacher = 1
    announce = courseo.announcements_set.all()
    return render(request, 'course/course.html', {'course': course, 'announcel': announce, 'is_teacher': is_teacher})


def course_add_user(request, course):
    user = get_username(request)
    if user == 'admin' or len(Course.objects.filter(title=course)[0].teachers.filter(name=user)) > 0:
        if request.method == 'GET':
            return render(request, 'course/course_add_user.html', {'course': course})
        elif request.method == 'POST':
            data = request.POST
            teachers = data.getlist('teacher')
            students = data.getlist('student')
            acourse = Course.objects.all().filter(title=course)[0]
            for x in teachers:
                teach = User.objects.all().filter(name=x)
                if len(teach) > 0:
                    teach = teach[0]
                    acourse.teachers.add(teach)
            for x in students:
                stud = User.objects.all().filter(name=x)
                if len(stud) > 0:
                    stud = stud[0]
                    acourse.students.add(stud)
            acourse.save()
            return redirect('/courses/'+course+'/add_user')
        else:
            return redirect('')
    else:
        return render(request, 'course/error.html')


def course_add_user_file(request, course):
    user = get_username(request)
    if user == 'admin' or len(Course.objects.filter(title=course)[0].teachers.filter(name=user)) > 0:
        if request.method == 'GET':
            return render(request, 'course/course_add_user.html', {'course': course})
        elif request.method == 'POST':
            upload_file = request.FILES['document'].read()
            upload_file = upload_file.decode("utf-8")
            reader = csv.reader(upload_file.split('\n'), delimiter=',')
            acourse = Course.objects.all().filter(title=course)[0]
            reader = reader[1:]
            for row in reader:
                if (row[0] == 'Instructor'):
                    teach = User.objects.all().filter(name=row[1])
                    if len(teach) > 0:
                        teach = teach[0]
                        acourse.teachers.add(teach)
                if (row[0] == 'Student'):
                    stud = User.objects.all().filter(name=row[1])
                    if len(stud) > 0:
                        stud = stud[0]
                        acourse.students.add(stud)
                acourse.save()
            return redirect('/')
        else:
            return redirect('/')
    else:
        return render(request, 'course/error.html')


def course_add_announce(request, course):           #mod by vinayaka
    user = get_username(request)
    if course_verify(course, user):
        if request.method == 'GET':
            return render(request, 'course/course_add_announce.html', {'course': course})
        elif request.method == 'POST':
            data = request.POST
            title = data['title']
            desc = data['desc']
            deadline = data['deadline']
            os.mkdir('media/' + course + '/' + title)
            os.mkdir('media/' + course + '/' + title + '/__grades')
            os.mkdir('media/' + course + '/' + title + '/__grades/man_grades')
            os.mkdir('media/' + course + '/' + title + '/__grades/auto_grades')
            os.mkdir('media/' + course + '/' + title + '/__grades/man_test')
            os.mkdir('media/' + course + '/' + title + '/__grades/auto_test')
            os.mkdir('media/' + course + '/' + title + '/__grades/auto_script')
            acourse = Course.objects.all().filter(title=course)[0]
            annobj = Announcements(title=title, desc=desc)
            annobj.course = acourse
            if len(deadline) > 0:
                deadline = deadline.split('T')
                dmy = deadline[0]
                time = deadline[1]
                dmy = dmy.split('-')
                time = time.split(':')
                dmy = [int(x) for x in dmy]
                time = [int(x) for x in time]
                [year, month, date] = dmy
                [hour, min] = time
                dobj = datetime(year, month, date, hour, min)
                annobj.end = dobj
            annobj.save()
            return redirect('/courses/' + course)
        else:
            return redirect('/courses/' + course)
    else:
        return render(request, 'course/error.html')


def course_modify_announce(request, course, announce):              #mod by jishnu
    announce = Announcements.objects.all().filter(title=announce)[0]
    if request.method == 'POST':
        data = request.POST
        title = data['title']
        desc = data['desc']
        deadline = data['deadline']
        annobj = announce
        annobj.title = title
        annobj.desc = desc
        if len(deadline) > 0:
            print(deadline)
            deadline = deadline.split('T')
            dmy = deadline[0]
            time = deadline[1]
            dmy = dmy.split('-')
            time = time.split(':')
            dmy = [int(x) for x in dmy]
            time = [int(x) for x in time]
            [year, month, date] = dmy
            [hour, min] = time
            dobj = datetime(year, month, date, hour, min)
            annobj.end = dobj
        annobj.save()
        return redirect('/courses/' + course + '/' + announce.title)
    elif request.method == 'GET':
        dobj = announce.end
        end_date = ''
        if dobj is not None:
            date = [dobj.year, dobj.month, dobj.day, dobj.hour, dobj.minute]
            date = [str(x) for x in date]
            for i in range(len(date)):
                if i > 0:
                    if len(date[i]) < 2:
                        date[i] = '0'+date[i]
            end_date = date[0]+'-'+date[1]+'-'+date[2]+'T'+date[3]+':'+date[4]
        return render(request, 'course/course_modify_announce.html', {'course': course, 'announce': announce,
                                                                      'end_date': end_date})
    else:
        return render(request, 'course/error.html')


def announce_page(request, course, announce):               #mod by vinayaka
    user = get_username(request)
    if not course_verify(course, user):
        return render(request, 'course/error.html')
    announce = Announcements.objects.all().filter(title=announce)
    if len(announce) > 0:
        announce = announce[0]
        cobj = announce.course
        is_teacher = 0
        if user == 'admin':
            is_teacher=1
        else:
            uobj = User.objects.all().filter(name=user)[0]
            if uobj in cobj.teachers.all():
                is_teacher = 1
        deadline = announce.end
        is_done = 0
        sub_exists=0
        dead_date = 'No deadline'
        if deadline is not None:
            dead_date = deadline.__str__()
            if deadline < timezone.now():
                is_done = 1
        fs = FileSystemStorage()
        sub_name = ''
        if fs.exists(course+'/'+announce.title+'/'+user):
            sub_exists = 1
            sub_name = fs.listdir(course+'/'+announce.title+'/'+user)[1][0]
        return render(request, 'course/announce.html', {'is_teacher': is_teacher, 'course': course,
                                                        'announce': announce, 'is_done': is_done,
                                                        'dead_date': dead_date, 'sub_exists': sub_exists,
                                                        'sub_name': sub_name, 'user': user})
    else:
        return render(request, 'course/error.html')


def add_course(request):
    user = get_username(request)
    if user == 'admin':
        if request.method == 'GET':
            return render(request, 'course/add_course.html')
        elif request.method == 'POST':
            data = request.POST
            title = data['title']
            teachers = data.getlist('teacher')
            acourse = Course.objects.all().filter(title=title)
            if len(acourse) > 0:
                acourse = acourse[0]
            else:
                acourse = Course(title=title)
                acourse.save()
            for x in teachers:
                teach = User.objects.all().filter(name=x)
                if len(teach) > 0:
                    teach = teach[0]
                    acourse.teachers.add(teach)
            acourse.save()
            return redirect('/')
        else:
            return redirect('/')
    else:
        return render(request, 'course/error.html')


def course_verify(course, user):
    cobj = Course.objects.filter(title=course)
    if len(cobj) > 0:
        cobj = cobj[0]
        if user == 'admin':
            return True
        if len(cobj.teachers.filter(name=user)) > 0 or len(cobj.students.filter(name=user)) > 0:
            return True
        else:
            return True
    else:
        return False


def get_username(request):
    return request.user.get_username()
