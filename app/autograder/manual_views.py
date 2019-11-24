from django.shortcuts import redirect
from .misc import *
import pickle


def get_all_sub_view(request, course, announce, file):      #vinayaka
    not_graded, graded = rem_students(course, announce, file)
    if len(not_graded) > 0:
        return redirect('/courses/'+course+'/'+announce+'/man_grade/'+file+'/user/'+not_graded[0])
    else:
        return render_view_page(request, course, announce, [file], '', 1, 100)


def get_user_sub_file(request, course, announce, file, name):       #vinayaka
    bef_file_name = file
    file = file.replace('-', '/')
    file = file.split('|')
    if request.method == 'POST':
        data = request.POST
        student_name_to_up = data['username']
        file_name = get_user_sub_name(course, announce, student_name_to_up)
        marks = int(data['marks'])
        tot_marks = int(data['tot_marks'])
        comment = data['comment']
        if not FileSystemStorage().exists(
                course + '/' + announce + '/__grades/man_grades/' + student_name_to_up + '.pickle'):
            sub_file = open(
                'media' + '/' + course + '/' + announce + '/__grades/man_grades/' + student_name_to_up + '.pickle',
                'wb+')
            pickle.dump([], sub_file)
            sub_file.close()
        sub_file = open(
            'media' + '/' + course + '/' + announce + '/__grades/man_grades/' + student_name_to_up + '.pickle', 'rb+')
        bef_list = pickle.load(sub_file)
        sub_file.close()
        print(bef_list)
        bef_list = [x for x in bef_list if not x[0] == file_name or not x[1] == file[0]]
        sub_file = open(
            'media' + '/' + course + '/' + announce + '/__grades/man_grades/' + student_name_to_up + '.pickle', 'wb+')
        bef_list.append([file_name, file[0], marks, tot_marks, comment])
        pickle.dump(bef_list, sub_file)
        sub_file.close()
        return redirect('/courses/'+course+'/'+announce+'/man_grade/'+bef_file_name)
    done = 0
    tot_marks = 100
    student_name = name
    return render_view_page(request, course, announce, student_name, file, done, tot_marks)


def get_user_sub_file_all(request, course, announce, file):     #vinayaka
    bef_file = file
    file = file.replace('-', '/')
    not_graded, graded = rem_students(course, announce, file)
    return render(request, 'autograder/man_list_student.html', {'bef_file': bef_file, 'not_graded': not_graded,
                                                                'graded': graded, 'course': course,
                                                                'announce': announce, 'file': file})


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


def get_man_csv(request, course, announce):     #vinayaka
    data = request.POST
    base = 'media/'+course+'/'+announce
    fil = open(base+'/__grades/man_grades.csv', 'w+')
    fil.close()
    choices = data.getlist('choose[]')
    bname = 0
    btname = 0
    if 'name' in choices:
        bname = 1
        choices.remove('name')
    if 'team_name' in choices:
        btname = 1
        choices.remove('team_name')
    gen_csv(base+'/__grades/man_grades', choices, bname, btname, base+'/__grades/man_grades.csv')
    return redirect('/media/'+course+'/'+announce+'/__grades/man_grades.csv')
