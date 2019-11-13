from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import zipfile
import io
import os


def submit_assign(request, course, announce):
    if request.user.is_authenticated:
        if request.method == 'POST':
            upload_file = request.FILES['document']
            fs = FileSystemStorage()
            user = request.user.get_username()
            if len(fs.listdir(course+'/'+announce+'/'+user)[1]) != 0:
                for fil in fs.listdir(course+'/'+announce+'/'+user)[1]:
                    fs.delete(course+'/'+announce+'/'+user+'/'+fil)  

            fs.save(course + '/' + announce + '/' + user+'/'+upload_file.name, upload_file)
        return render(request, 'files/upload.html',{'course' : course, 'announce' :announce})
    else:
        return redirect('account/login')



def submit_assign_mass(request, course, announce):
    if request.user.is_authenticated:
        if request.method == 'POST':
            upload_file = request.FILES['document']
            with zipfile.ZipFile(upload_file,'r') as f:
                for name in f.namelist():
                    data = f.read(name)
                    if len(name.split('/')) == 3 and not(name.split('/')[2] == ''):
                        fs = FileSystemStorage()
                        k = name.split('/')
                        tail = k[1]+'/'+k[2] 
                        if len(fs.listdir(course+'/'+announce+'/'+k[1])[1]) != 0:
                            for fil in  fs.listdir(course+'/'+announce+'/'+k[1])[1]:
                                fs.delete(course+'/'+announce+'/'+k[1]+'/'+fil)                          
                        fs.save(course+'/'+announce+'/'+tail, io.BytesIO(data))

        return render(request, 'files/upload.html',{'course' : course, 'announce' :announce})
    else:
        return redirect('account/login')


def get_assign(request, course, announce):
    print('first')
    if request.user.is_authenticated:
        print('second')
        if request.method == 'POST':
            print('third')
            s = getzip(course, announce)
            resp = HttpResponse(s.getvalue(), content_type='application/x-zip-compressed')
            resp['Content-Disposition'] = 'attachment; filename=%s' % (course + '-' + announce + '.zip')
            return resp
        return render(request, 'files/download.html',{'course' : course, 'announce' :announce})
    else:
        return redirect('account/login')


def getzip(course, assign):
    fs = FileSystemStorage()
    dir_fil=course+'/'+assign+'/'
    subdirs, files = fs.listdir(dir_fil)
    print(files)
    s = io.BytesIO()
    zipf = zipfile.ZipFile(s, "w")
    for file in files:
        zipf.write(settings.MEDIA_ROOT+'/'+dir_fil+file, file)
    zipf.close()
    return s

