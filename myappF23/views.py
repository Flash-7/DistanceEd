from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Student, Category, Course, Instructor, Order
from .forms import InterestForm, OrderForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import datetime, timedelta

# Create your views here.
# def index(request):
#     http_response = HttpResponse()

#     head = "<head><style>body{margin:0}</style></head>"
#     http_response.write(head)

#     heading = "<h1 style='text-align: center;background-color: #0078d4;color: #fff;padding:12px 0'> Welcome to Distance-Ed Web App </h1>"
#     http_response.write(heading)

#     category_list = Category.objects.all().order_by('id')[:10]
#     course_list = Course.objects.all().order_by('level')[:5]

#     category_item = ""
#     course_item = ""

#     for category in category_list:
#         category_item += f"<li>{category}</li>"

#     for course in course_list:
#         course_item += f"<li>{course} &ensp; $: {course.price} &ensp; lvl: {course.level}</li>"

#     column1 = f"<div style='flex:50%;padding-left:15%'><h3> List of categories: </h3><ul>{category_item}</ul></div>"
#     column2 = f"<div style='flex:50%;padding-left:15%'><h3> List of courses: </h3><ul style='margin-left:-10%'>{course_item }</ul></div>"
#     row1 = f"<div style='display:flex'>{column1} {column2}</div>"

#     http_response.write(row1)

#     return http_response

# def detail(request, category_no):
#     category = get_object_or_404(Category, pk=category_no)
#     http_response = HttpResponse()

#     head = "<head><style>body{margin:0}</style></head>"
#     http_response.write(head)

#     heading = "<h1 style='text-align: center;background-color: #0078d4;color: #fff;padding:12px 0'> Distance-Ed Web App </h1>"
#     http_response.write(heading)

#     heading = f"<h2 style='text-align:center'>Category: {category.name}</h1>"
#     http_response.write(heading)

#     course_list = category.course_set.all()
#     course_item = ""

#     for course in course_list:
#         course_item += f"<li><strong>{course.title}</strong><br><p>Description: {course.description}<br>$: {course.price} &emsp; lvl: {course.level}</p></li>"

#     category_courses = f"<div><h3 style='text-align:center'>Course list:</h3><ul style='padding-left:38%'>{course_item}</ul></div>"

#     http_response.write(category_courses)

#     return http_response

# def about(request):
#     http_response = HttpResponse()

#     head = "<head><style>body{margin:0}</style></head>"
#     http_response.write(head)

#     heading = "<h1 style='text-align: center;background-color: #0078d4;color: #fff;padding:12px 0'> Distance-Ed Web App </h1>"
#     http_response.write(heading)

#     para = "<p style='text-align:center'>This is a Distance Education Website! Search our Categories to find all available Courses.</p>"
#     http_response.write(para)

#     return http_response


# def index(request):
#     category_list = Category.objects.all().order_by('id')[:10]
#     course_list = Course.objects.all().order_by('-price')[:]
#     return render(request, 'myappF23/index0.html', {'category_list': category_list, 'course_list': course_list})


# def detail(request, category_no):
#     category = get_object_or_404(Category, pk=category_no)
#     course_list = category.course_set.all()
#     return render(request, 'myappF23/detail0.html', {'category': category, 'course_list': course_list})


# def about(request):
#     return render(request, 'myappF23/about0.html')


# def instructor_courses(request, instructor_id):
#     instructor = get_object_or_404(Instructor, pk=instructor_id)
#     courses_taught = Course.objects.filter(instructors=instructor)

#     # Create a dictionary with the course as the key and its students as the value
#     students_by_course = {}
#     for course in courses_taught:
#         students_by_course[course] = course.students.all()

#     return render(request, 'myappF23/instructorCourses.html', {'instructor': instructor,'students_by_course': students_by_course,})


def index(request):
    user_visits = request.COOKIES.get('user_visits', 0)
    last_login_info = request.session.get('last_login_info')
    user_visits = int(user_visits) + 1

    category_list = Category.objects.all().order_by('id')[:10]
    course_list = Course.objects.all().order_by('-price')[:5]

    context = {'category_list': category_list, 'course_list': course_list, 'user_visits': user_visits, 'last_login_info': last_login_info}
    response = render(request, 'myappF23/index.html', context)
    response.set_cookie('user_visits', user_visits, max_age=10)
    return response


def detail(request, category_no):
    category = get_object_or_404(Category, pk=category_no)
    course_list = category.course_set.all()
    return render(request, 'myappF23/detail.html', {'category': category, 'course_list': course_list})


def about(request):
    visits = request.COOKIES.get('user_visits', 0)
    return render(request, 'myappF23/about.html', {'visits': visits})


def instructor_courses(request, instructor_id):
    instructor = get_object_or_404(Instructor, pk=instructor_id)
    courses_taught = Course.objects.filter(instructors=instructor)

    # Create a dictionary with the course as the key and its students as the value
    students_by_course = {}
    for course in courses_taught:
        students_by_course[course] = course.students.all()

    return render(request, 'myappF23/instructorCourses.html',
                  {'instructor': instructor, 'students_by_course': students_by_course, })


def courses(request):
    courselist = Course.objects.all().order_by('id')
    return render(request, 'myappF23/courses.html', {'courselist': courselist})


def place_order(request):
    msg = ''
    courselist = Course.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)

            if int(order.levels) > int(order.courses.level):
                msg = 'You exceeded the number of levels for this course.'
                return render(request, 'myappF23/order_response.html', {'msg': msg})
            else:
                order.save()
                if order.courses.price > 150.00:
                    order.discount()
                msg = 'Your course has been ordered successfully.'
                return render(request, 'myappF23/order_response.html', {'msg': msg})

        else:
            msg = 'Form is not valid.'
    else:
        form = OrderForm()
    return render(request, 'myappF23/place_order.html', {'form': form, 'msg': msg, 'courselist': courselist})



def coursedetail(request, course_id):
    course = Course.objects.get(pk=course_id)

    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid() and form.cleaned_data['interested'] == 1:
            course.interested += 1
            course.interested_students.add(Student.objects.filter(user=request.user).first())
            course.save()
            return redirect('myappF23:index')  # Redirect to the main index page after indicating interest
    else:
        form = InterestForm()

    return render(request, 'myappF23/coursedetail.html', {'course': course, 'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)

                current_login_info = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                request.session['last_login_info'] = current_login_info
                request.session.set_expiry(300)

                return HttpResponseRedirect(reverse('myappF23:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myappF23/login.html')


@login_required
def user_logout(request):
    if 'last_login_info' in request.session:
        del request.session['last_login_info']
    return HttpResponseRedirect(reverse('myappF23:index'))

@login_required
def myaccount(request):
    logged_in_user = request.user
    logged_in_student = Student.objects.filter(user=logged_in_user).first()
    if logged_in_student is not None:
        orders = logged_in_student.order_set.all()
        interested_courses = Course.objects.filter(interested_students=logged_in_student)
        return render(request, 'myappF23/myaccount.html', {'student': logged_in_student, 'orders': orders, 'interested_courses': interested_courses})
    else:
        return HttpResponse('You are not a registered student!')


def set_test_cookie(request):
    response = HttpResponse("Test cookie set!")
    response.set_cookie('test_cookie', 'test_cookie', max_age=3600)  # Set max_age as desired expiration time in seconds
    return response


def check_test_cookie(request):
    if 'test_cookie' in request.COOKIES:
        cookie_value = request.COOKIES['test_cookie']
        return HttpResponse(f"Test cookie worked! Value: {cookie_value}")
    else:
        return HttpResponse("Test cookie not present.")


def delete_test_cookie(request):
    response = HttpResponse("Test cookie deleted!")
    response.delete_cookie('test_cookie')
    return response


# Make the user’s session cookies to expire when the user’s web browser is closed instead of 5 minutes.

# i) do you need to change anything in your view functions?
# - To make the user's session cookies expire when the user's web browser is closed, you don't need to change anything in your view functions. The default behavior of Django sessions is to expire when the user's browser is closed.

# ii) what setting you use to do that? 
# -  you can set the SESSION_COOKIE_AGE setting in your settings.py file to None. This setting controls the age of session cookies in seconds. When set to None, session cookies will expire when the user's browser is closed.