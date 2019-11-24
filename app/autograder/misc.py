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
