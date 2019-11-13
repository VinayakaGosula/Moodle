from django.contrib import admin
from django.urls import path, include
from app import views


urlpatterns = [
    #path('admin/', admin.site.urls),
    #accounts
    path('', views.login_index, name='login_index'),
    path('account/register', views.register, name='register'),
    path('account/', include('django.contrib.auth.urls')),
    #courses
    path('admin/add_course', views.add_course, name='add_course'),
    path('courses/', views.index, name='course_home'),
    path('courses/<str:course>/add_user', views.course_add_user, name='course_add_user'),
    path('courses/<str:course>/add_user_file', views.course_add_user_file, name='course_add_user_file'),
    path('courses/<str:course>/add_announce', views.course_add_announce, name='course_add_announce'),
#    path('admin/courses/change', views.course_user_change, name='course_user_change'),
    path('courses/<str:course>', views.course_page, name='course'),
    path('courses/<str:course>/<str:announce>', views.announce_page, name='announce'),

    #files
    path('courses/<str:course>/<str:announce>/submit', views.submit_assign, name='submit_page'),
    path('courses/<str:course>/<str:announce>/get', views.get_assign, name='get_page')
]
