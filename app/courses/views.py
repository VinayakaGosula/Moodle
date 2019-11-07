from django.shortcuts import render, redirect
from ..models import *


def index(request):
    if request.user.is_authenticated:
        user = get_username(request)
        if user == 'admin':
            tcourses = Course.objects.all()
            scourses = []
            return render(request, 'course/index.html', {'tcourses': tcourses, 'scourses': scourses})

        uobject = User.objects.all().filter(name=user)
        tcourses = []
        scourses = []
        if len(uobject) > 0:
            tcourses = uobject[0].course_teacher.all()
            scourses = uobject[0].course_student.all()
        return render(request, 'course/index.html', {'tcourses': tcourses, 'scourses': scourses})
    else:
        return redirect('account/login')


def course_page(request, course):
    user = get_username(request)
    if not course_verify(course, user):
        return render(request, 'course/error.html')
    courseo = Course.objects.all().filter(title=course)[0]
    uobj = User.objects.all().filter(name=user)[0]
    is_teacher = 0
    if uobj in courseo.teachers.all():
        is_teacher = 1
    announce = courseo.announcements_set.all()
    return render(request, 'course/course.html', {'course': course, 'announcel': announce, 'is_teacher' : is_teacher})


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
            return redirect('/')
        else:
            return redirect('/')
    else:
        return render(request, 'course/error.html')


def course_add_announce(request, course):
    user = get_username(request)
    if course_verify(course, user):
        if request.method == 'GET':
            return render(request, 'course/course_add_announce.html', {'course': course})
        elif request.method == 'POST':
            data = request.POST
            title = data['title']
            desc = data['desc']
            acourse = Course.objects.all().filter(title=course)[0]
            annobj = Announcements(title=title, desc=desc)
            annobj.course = acourse
            annobj.save()
            return redirect('/courses/'+course)
        else:
            return redirect('/courses/'+course)
    else:
        return render(request, 'course/error.html')


def announce_page(request, course, announce):
    user = get_username(request)
    if not course_verify(course, user):
        return render(request, 'course/error.html')
    announce = Announcements.objects.all().filter(title=announce)
    if len(announce) > 0:
        announce = announce[0]
        cobj = announce.course
        uobj = User.objects.all().filter(name=user)[0]
        is_teacher = 0
        if uobj in cobj.teachers.all():
            is_teacher = 1
        return render(request, 'course/announce.html', {'is_teacher': is_teacher, 'course': course, 'announce': announce})
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
