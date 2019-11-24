from django.core.files.storage import FileSystemStorage
import zipfile
from django.conf import settings
import pickle
import os


def extract_sub(course, assign, user):      #hemant
    fs = FileSystemStorage()
    user_file_path = course + '/' + assign + '/' + user
    if fs.exists(user_file_path):
        if len(fs.listdir(user_file_path)[1]) > 0:
            file_name = fs.listdir(user_file_path)[1][0]
            if not fs.exists(user_file_path + '/' + file_name.rstrip('.zip')):
                zipf = zipfile.ZipFile(settings.MEDIA_ROOT + '/' + user_file_path + '/' + file_name)
                zipf.extractall(settings.MEDIA_ROOT + '/' + user_file_path)


def get_user_sub_name(course, assign, user):    #hemant
    fs = FileSystemStorage()
    user_file_path = course + '/' + assign + '/' + user
    if fs.exists(user_file_path) and len(fs.listdir(user_file_path)[1]) > 0:
        file_name = fs.listdir(user_file_path)[1][0]
        return file_name.rstrip('.zip')
    return ''


def convert_file(inp):      #hemant
    out = []
    cur_dep = -1
    cur_path = ''
    cur_inp = inp
    cnt = 1
    while len(cur_inp) > 0:
        cur_line = cur_inp[:cur_inp.find('\n')]
        cur_inp = cur_inp[cur_inp.find('\n') + 1:]
        strip_line = cur_line.lstrip('\t')
        depth = len(cur_line) - len(strip_line)
        while cur_dep >= depth:
            cur_path = cur_path[:cur_path.rfind('/')]
            cur_dep -= 1
        file_name = cur_line[:cur_line.find('|')].lstrip('\t')
        cur_line = cur_line[cur_line.find('|') + 1:]
        args = cur_line.split(',')
        cur_path = cur_path + '/' + file_name
        cur_dep += 1
        if args[0] == '1':
            if args[1] == '1':
                out.append([file_name, cur_path.lstrip('/'), args[2]])
            else:
                out.append([file_name, cur_path.lstrip('/   ')])
        cnt -= 1
    return out


def run_file(course, announce, file_path, user):        #vinayaka
    fs = FileSystemStorage()
    file = fs.open(course + '/' + announce + '/man_grade.txt')
    inp = file.read()
    file.close()
    out = convert_file(inp.decode('utf-8'))
    lis = [x for x in out if x[1] == file_path]
    if len(lis) > 0:
        lis = lis[0]
        if len(lis) == 3:
            command, path = update_paths_man_grade(lis[2], course, announce, user)
            path = path + '/' + file_path
            if path.rfind('/') == -1:
                path = ''
            else:
                path = path[:path.rfind('/')]
            run_command(command, path)


def update_paths_man_grade(inp, course, announce, student):     #vinayaka
    test_path = os.path.abspath('media/' + course + '/' + announce + '/__grades/man_test/' +
                                get_user_sub_name(course, announce, '__grades/man_test'))
    sub_path = 'media/' + course + '/' + announce + '/' + student + '/' + get_user_sub_name(course, announce, student)
    return inp.replace('{{test_root}}', test_path), sub_path


def run_command(command, dir):      #vinayaka
    if os.path.exists(dir):
        subprocess.call(command, cwd=dir, shell=True)


def render_view_page(request, course, announce, user, file_list, done, tot_marks):      #vinayaka
    loc = []
    if not done:
        for file_name in file_list:
            loc.append(
                '/media' + '/' + course + '/' + announce + '/' + user + '/' + get_user_sub_name(course, announce, user) \
                + '/' + file_name)
        extract_sub(course, announce, user)
        run_file(course, announce, file_list[0], user)
    exists = [x for x in loc if FileSystemStorage().exists(x.lstrip('/media/'))]
    return render(request, 'autograder/manual_viewer.html', {'loc': loc,
                                                             'done': done, 'course': course, 'announce': announce,
                                                             'file': ('|'.join(file_list)).replace('/', '-'),
                                                             'user': user,
                                                             'tot_marks': tot_marks,
                                                             'exists': exists})


def rem_students(course, announce, file):       #vinayaka
    fs = FileSystemStorage()
    file = file.replace('-', '/')
    student_list = fs.listdir(course + '/' + announce)[0]
    student_list.remove('__grades')
    to_be_graded = []
    for x in student_list:
        fil_path = 'media/' + course + '/' + announce + '/__grades/man_grades/' + x + '.pickle'
        if os.path.exists(fil_path):
            f = open(fil_path, 'rb')
            data = pickle.load(f)
            f.close()
            is_present = 0
            for y in data:
                if y[1] == file:
                    is_present = 1
            if not is_present:
                to_be_graded.append(x)
    graded = [x for x in student_list if x not in to_be_graded]
    return to_be_graded, graded
