from functools import partial
from django.core.files.storage import FileSystemStorage
import zipfile
import subprocess
import shutil
from django.shortcuts import render
from django.conf import settings
from multiprocessing.pool import ThreadPool
from .csvgen import *


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
                out.append([file_name, cur_path.lstrip('/')])
        cnt -= 1
    return out


def convert_file_with_dir(inp):      #hemant
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
        cur_path = cur_path + '/' + file_name
        cur_dep += 1
        if file_name != '':
            out.append([file_name, cur_path.lstrip('/')])
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


def update_paths_auto_grade(course, announce):      #jishnu
    test_path = '../../__grades/auto_test/' + get_user_sub_name(course, announce, '__grades/auto_test')
    script_path = 'media/' + course + '/' + announce + '/__grades/auto_script/' + get_user_sub_name(course, announce, '__grades/auto_script')
    return os.path.abspath(test_path), '../../..', script_path


def gen_auto_out(user, sub_name, data, course, assign):     #jishnu
    data = data.split('\n\n')
    data = [x for x in data if x != '']
    data = [x.split('\n') for x in data]
    for i in range(len(data)):
        data[i] = [x for x in data[i] if x != '']
        comm = ''

        for k in range(len(data[i])):
            if k > 2:
                comm += data[i][k]
        data[i] = [sub_name, data[i][0], int(data[i][1]), int(data[i][2]), comm]
    pfile = open('media/'+course+'/'+assign+'/__grades/auto_grades/'+user+'.pickle', 'wb+')
    pickle.dump(data, pfile)
    pfile.close()
    return data


def eval_one(submission, script, command, testcases, course, assign):       #jishnu
    command = command.replace("{submission}", submission)
    command = command.replace("{testcases}", testcases)
    data = subprocess.check_output(command, cwd=script, shell=True)
    data = data.decode('utf-8')
    user = submission.split('/')[-2]
    file_name = submission.split('/')[-1]
    gen_auto_out(user, file_name, data, course, assign)
    return [submission.split('/')[-2], data]


def eval_all(script, submissions, command, testcases, course, assign, skips): #jishnu
    files = os.listdir('media/'+course+'/'+assign)
    files = [x for x in files if os.path.isdir('media/'+course+'/'+assign+'/' + x)]
    filelist=[]
    for i in range(len(files)):
        if files[i] != '__grades' and files[i] not in skips:
            filelist.append(submissions + '/' + files[i] + '/' + get_user_sub_name(course, assign, files[i]))
    p = ThreadPool(processes=len(filelist))
    data = p.map(partial(eval_one, script=script, command=command, testcases=testcases,
                         course=course, assign=assign), filelist)
    p.close()
    return data


def reauto_start(course, assign):       #jishnu
    test, sub, script = update_paths_auto_grade(course, assign)
    if os.path.exists('media/'+course+'/'+assign+'/__grades/auto_grades'):
        shutil.rmtree('media/'+course+'/'+assign+'/__grades/auto_grades')
    os.mkdir('media/'+course+'/'+assign+'/__grades/auto_grades')
    if os.path.exists('media/'+course+'/'+assign+'/auto_grade.txt'):
        f = open('media/'+course+'/'+assign+'/auto_grade.txt')
        command = f.read()
        f.close()
        if len(command) > 0:
            return eval_all(script, sub, command, test, course, assign, [])
    return 0


def auto_start(course, assign):     #jishnu
    test, sub, script = update_paths_auto_grade(course, assign)
    if not os.path.exists('media/'+course+'/'+assign+'/__grades/auto_grades'):
        os.mkdir('media/'+course+'/'+assign+'/__grades/auto_grades')
    if os.path.exists('media/'+course+'/'+assign+'/auto_grade.txt'):
        f = open('media/'+course+'/'+assign+'/auto_grade.txt')
        command = f.read()
        f.close()
        if len(command) > 0:
            skip = os.listdir('media/'+course + '/' + assign + '/__grades/auto_grades')
            skip = [x.rstrip('.pickle') for x in skip]
            return eval_all(script, sub, command, test, course, assign, skip)
    return 0


def get_auto_len(course, assign):       #jishnu
    fs = FileSystemStorage()
    return [len(os.listdir('media/'+course+'/'+assign+'/__grades/auto_grades')), len(fs.listdir(course+'/'+assign)[0])-1]
