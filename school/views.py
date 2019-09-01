from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import Course, Student, User
from .forms import CourseForm, CustomUserCreationForm, SigninForm, StudentForm, CustomUserChangeForm

def course_list(request):
	courses = Course.objects.all()
	context = {
		"courses": courses,
	}
	return render(request, 'course_list.html', context)


def course_detail(request, course_id):
	course = Course.objects.get(id=course_id)
	context = {
		"course": course,
        "students": Student.objects.filter(course_id=course_id),
	}
	return render(request, 'course_detail.html', context)


def course_create(request):
	if request.user.is_anonymous:
		return redirect('signin')
	form = CourseForm()
	if request.method == "POST":
		form = CourseForm(request.POST, request.FILES or None)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Created!")
			return redirect('course-list')
		print (form.errors)
	context = {
	"form": form,
	}
	return render(request, 'create_course.html', context)


def course_update(request, course_id):
	course = Course.objects.get(id=course_id)
	form = CourseForm(instance=course)
	if request.method == "POST":
		form = CourseForm(request.POST, request.FILES or None, instance=course)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Edited!")
			return redirect('course-list')
		print (form.errors)
	context = {
	"form": form,
	"course": course,
	}
	return render(request, 'update_course.html', context)


def course_delete(request, course_id):
	Course.objects.get(id=course_id).delete()
	messages.success(request, "Successfully Deleted!")
	return redirect('course-list')

def signin(request):
    form = SigninForm()
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('course-list')
    context = {
        "form":form
    }
    return render(request, 'signin.html', context)

def signout(request):
    logout(request)
    return redirect('course-list')

def signup(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(user.password)
            user.save()

            login(request, user)
            return redirect("course-list")
    context = {
        "form":form,
    }
    return render(request, 'signup.html', context)

def noaccess(request):

	return render(request, 'noaccess.html')


def add_student(request, course_id):
    course_obj = Course.objects.get(id=course_id)
    form = StudentForm(instance=course_obj)
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():

            studentx = form.save(commit=False)
            studentx.course = course_obj

            studentx.save()
            return redirect('course-detail', course_id)
    
    context = {
        "course_obj": course_obj,
        "form":form,
    }

    return render(request, 'add_student.html', context)
