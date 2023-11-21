from django.urls import path
from myappF23 import views 

app_name = 'myappF23'

# urlpatterns = [
#     path(r'', views.index, name='index'),
#     path('<int:category_no>/', views.detail, name='detail'),
#     path('aboutwebapp/', views.about, name='about')
# ]

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('<int:category_no>/', views.detail, name='detail'),
    path('instructorDetails/<int:instructor_id>/', views.instructor_courses, name='instructor_courses'),
    path('courses/', views.courses, name='courses'),
    path('courses/<int:course_id>/', views.coursedetail, name='coursedetail'),
    path('place_order/', views.place_order, name='place_order'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('set/', views.set_test_cookie, name='set_test_cookie'),
    path('check/', views.check_test_cookie, name='check_test_cookie'),
    path('delete/', views.delete_test_cookie, name='delete_test_cookie'),
]