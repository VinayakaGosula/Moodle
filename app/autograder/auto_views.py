from django.shortcuts import render, redirect
from .misc import *


def auto_grade_page(request, course, announce):         #hemant
    exists = 0
    fs = FileSystemStorage()
    if fs.exists(course+'/'+announce+'/auto_grade.txt'):
        exists = 1
    base = 'media/'+course+'/'+announce
    csv_cols = []
    if os.path.exists(base+'/auto_grade.txt'):
        base1 = base+'/__grades/auto_grades'
        if os.path.exists(base1):
            if len(os.listdir(base1)):
                file_name = os.listdir(base1)[0]
                file_name = base1+'/'+file_name
                file = open(file_name, 'rb')
                csv_cols = pickle.load(file)
                file.close()
                csv_cols = [x[1] for x in csv_cols]
                csv_cols.append('name')
                csv_cols.append('team_name')
    return render(request, 'autograder/auto_grade.html', {'exists': exists,
                                                          'course': course, 'announce': announce, 'csv_cols': csv_cols})


def add_auto_file(request, course, announce):   #hemant
    files = request.FILES
    if 'auto_file' in files.keys():
        upload_file = files['auto_file']
        fs = FileSystemStorage()
        file_path = course + '/' + announce + '/__grades/auto_script/auto_script.zip'
        if fs.exists(file_path):
            fs.delete(file_path)
        fs.save(file_path, upload_file)
        extract_sub(course, announce, '__grades/auto_script')
    if 'test_file' in files.keys():
        upload_file = files['test_file']
        fs = FileSystemStorage()
        file_path = course + '/' + announce + '/' + '__grades/auto_test/auto_test.zip'
        if fs.exists(file_path):
            fs.delete(file_path)
        fs.save(file_path, upload_file)
        extract_sub(course, announce, '__grades/auto_test')
    data_in = request.POST
    command_to = data_in['command']
    command_to = command_to.lstrip(" ")
    if len(command_to) > 0:
        auto_file = open('media/'+course+'/'+announce+'/auto_grade.txt', 'w+')
        auto_file.write(command_to)
        auto_file.close()
    return redirect('/courses/' + course + '/' + announce + '/auto_grade')
