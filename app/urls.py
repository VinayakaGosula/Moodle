from django.contrib import admin
from django.urls import path, include
from app import views


urlpatterns = [
    #path('admin/', admin.site.urls),
    #accounts
    path('', views.login_index, name='login_index'),
    path('account/register', views.register, name='register'),
    path('account/', include('django.contrib.auth.urls'))
]
