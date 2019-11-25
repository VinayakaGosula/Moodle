from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import zipfile
import io


def submit_assign(request, course, announce):               #mod by hemant
    if request.user.is_authenticated:
        if request.method == 'POST':
            upload_file = request.FILES['document']
            fs = FileSystemStorage()
            user = request.user.get_username()
            user_file_path = course + '/' + announce + '/' + user
            if fs.exists(user_file_path) and (fs.listdir(user_file_path)[1]) != 0:
                for fil in fs.listdir(user_file_path)[1]:
                    fs.delete(user_file_path + '/' + fil)
            fs.save(user_file_path + '/' + upload_file.name, upload_file)
        return render(request, 'files/upload.html', {'course': course, 'announce': announce})
    else:
        return redirect('account/login')


def submit_assign_mass(request, course, announce):          #mod by hemant
    if request.user.is_authenticated:
        if request.method == 'POST':
            upload_file = request.FILES['document']
            with zipfile.ZipFile(upload_file, 'r') as f:
                for name in f.namelist():
                    data = f.read(name)
                    if len(name.split('/')) == 3 and not (name.split('/')[2] == ''):
                        fs = FileSystemStorage()
                        k = name.split('/')
                        tail = k[1] + '/' + k[2]
                        file_path = course + '/' + announce + '/' + k[1]
                        if fs.exists(file_path) and (fs.listdir(file_path)[1]) != 0:
                            for fil in fs.listdir(file_path)[1]:
                                fs.delete(file_path + '/' + fil)
                        fs.save(course + '/' + announce + '/' + tail, io.BytesIO(data))

        return render(request, 'files/upload.html', {'course': course, 'announce': announce})
    else:
        return redirect('account/login')


def get_assign(request, course, announce):                  #mod by hemant
    if request.user.is_authenticated:
        if request.method == 'POST':
            s = getzip(course, announce)
            resp = HttpResponse(s.getvalue(), content_type='application/x-zip-compressed')
            resp['Content-Disposition'] = 'attachment; filename=%s' % (course + '-' + announce + '.zip')
            return resp
        fs = FileSystemStorage()
        sublist = []
        subpath = []
        if fs.exists(course+'/'+announce):
            dirs = fs.listdir(course+'/'+announce)
            dirs = dirs[0]
            dirs.remove('__grades')
            sublist = dirs
            for x in dirs:
                sub_name = fs.listdir(course+'/'+announce+'/'+x)[1][0]
                subpath.append('/media/'+course+'/'+announce+'/'+x+'/'+sub_name)
        return render(request, 'files/download.html', {'course': course, 'announce': announce,
                                                       'sublist': list(zip(sublist, subpath))})
    else:
        return redirect('account/login')


def getzip(course, assign):
    fs = FileSystemStorage()
    dir_fil = course + '/' + assign + '/'
    files, subdir = fs.listdir(dir_fil)
    s = io.BytesIO()
    zipf = zipfile.ZipFile(s, "w")
    for file in files:
        if file != '__grades':
            file_name = fs.listdir(dir_fil+file)[1][0]
            zipf.write(settings.MEDIA_ROOT + '/' + dir_fil + file+'/'+file_name, file+'/'+file_name)
    zipf.close()
    return s
