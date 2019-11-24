from django.shortcuts import redirect,render
from .misc import *
import pickle


def man_grade_page(request, course, announce):      #hemant
    exists = 0
    fs = FileSystemStorage()
    names = []
    paths = []
    csv_cols = []
    if fs.exists(course+'/'+announce+'/man_grade.txt'):
        exists = 1
        fs = FileSystemStorage()
        file = fs.open(course+'/'+announce+'/man_grade.txt')
        inp = file.read()
        file.close()
        out = convert_file(inp.decode('utf-8'))
        names = [x[0] for x in out]
        paths = [x[1].replace('/', '-') for x in out]
        csv_cols = [x[1] for x in out]
        csv_cols.append('name')
        csv_cols.append('team_name')
    return render(request, 'autograder/man_grade.html', {'exists': exists, 'names': names, 'paths': paths,
                                                         'course': course, 'announce': announce, 'csv_cols': csv_cols})


def add_man_file(request, course, announce):        #hemant
    files = request.FILES
    if 'man_file' in files.keys():
        upload_file = files['man_file']
        fs = FileSystemStorage()
        file_path = course + '/' + announce + '/' + 'man_grade.txt'
        if fs.exists(file_path):
            fs.delete(file_path)
        fs.save(file_path, upload_file)
    if 'test_file' in files.keys():
        upload_file = files['test_file']
        fs = FileSystemStorage()
        file_path = course + '/' + announce + '/' + '__grades/man_test/' + 'man_test.zip'
        if fs.exists(file_path):
            fs.delete(file_path)
        fs.save(file_path, upload_file)
        extract_sub(course, announce, '__grades/man_test')
    return redirect('/courses/' + course + '/' + announce + '/man_grade')