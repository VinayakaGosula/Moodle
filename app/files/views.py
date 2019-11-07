from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import zipfile
import io


def submit_assign(request, course, announce):
    if request.user.is_authenticated:
        if request.method == 'POST':
            upload_file = request.FILES['document']
            fs = FileSystemStorage()
            fs.save(course + '/' + announce + '/' + upload_file.name, upload_file)
        return render(request, 'files/upload.html')
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
        return render(request, 'files/download.html')
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

