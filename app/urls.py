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
    path('courses/<str:course>/<str:announce>/get', views.get_assign, name='get_page'),
    path('courses/<str:course>/<str:announce>/submit_mass', views.submit_assign_mass, name='submit_mass_page'),

    # autograding
    path('courses/<str:course>/<str:announce>/man_grade', views.man_grade_page, name='man_grade_page'),                         #hemant
    path('courses/<str:course>/<str:announce>/man_grade/add_man_grade_file', views.add_man_file, name='add_man_grade'),         #hemant
    path('courses/<str:course>/<str:announce>/man_grade/get_csv', views.get_man_csv, name='man_get_csv'),  # vinayaka
    path('courses/<str:course>/<str:announce>/man_grade/<str:file>', views.get_all_sub_view, name='manual_viewer'),
    path('courses/<str:course>/<str:announce>/man_grade/<str:file>/list', views.get_user_sub_file_all,name='man_sub_list'),  # vinayaka
    path('courses/<str:course>/<str:announce>/man_grade/<str:file>/user/<str:name>', views.get_user_sub_file,name='user_sub_view'),#vinayaka


    path('courses/<str:course>/<str:announce>/auto_grade', views.auto_grade_page, name='auto_grade_page'),                      #hemant
    path('courses/<str:course>/<str:announce>/auto_grade/add_auto_grade_file',views.add_auto_file, name='add_auto_grade'),      #hemant
]
