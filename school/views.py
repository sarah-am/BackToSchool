from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .models import Semester, Classroom, Student, Attendance
from .forms import StudentForm, SignupForm, SigninForm, SemesterForm, ClassroomForm, AttendanceForm
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from django.utils import timezone


### SEMESTERS ###
def semester_list(request):
    semesters = Semester.objects.all().order_by('year')
    classrooms = Classroom.objects.filter(semester__in=semesters, pk=request.user.pk).order_by('title')
    students = Student.objects.filter(classroom__in=classrooms)
    attendance = Attendance.objects.filter(student__in=students)

    context = {
        "semesters": semesters,
        "classrooms": classrooms,
        "students": students
    }
    return render(request, 'semester_list.html', context)

def semester_create(request):
    if request.user.is_anonymous:
        return redirect('signin')
    form = SemesterForm()
    if request.method == "POST":
        form = SemesterForm(request.POST, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('semester-list') 
        print (form.errors)
    context = {
        "form": form,
    }
    return render(request, 'create_semester.html', context)

def semester_update(request, semester_id):
    semester = Semester.objects.get(id=semester_id)
    if request.user.is_authenticated:
        form = SemesterForm(instance=semester)
        if request.method == "POST":
            form = SemesterForm(request.POST, instance=semester)
            if form.is_valid():
                form.save()
                return redirect('semester-list')
            print (form.errors)
    context = {
    "form": form,
    "semester": semester,
    }
    return render(request, 'update_semester.html', context)

### CLASSROOMS ###
def classroom_create(request, semester_id):
    form = ClassroomForm()
    semester = Semester.objects.get(id=semester_id)
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ClassroomForm(request.POST)
            if form.is_valid():
                classroom = form.save(commit=False)
                classroom.semester = semester
                classroom.teacher = request.user
                classroom.save()
                return redirect('semester-list')
            print (form.errors)
    context = {
        "form": form,
        "semester": semester,
    }
    return render(request, 'create_classroom.html', context)

def classroom_update(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    if request.user.is_authenticated:
        form = ClassroomForm(instance=classroom)
        if request.method == "POST":
            form = ClassroomForm(request.POST, instance=classroom)
            if form.is_valid():
                form.save()
                return redirect('my-classrooms-detail', classroom_id)
            print (form.errors)
    context = {
    "form": form,
    "classroom": classroom,
    }
    return render(request, 'update_classroom.html', context)

def classroom_delete(request, semester_id, classroom_id):
    Semester.objects.get(id=semester_id)
    if request.user.is_authenticated:
        Classroom.objects.get(id=classroom_id).delete()
        return redirect('semester-list')

#### Teacher ####
def myclasses_detail(request, classroom_id):
    today = timezone.now().date()
    classroom = Classroom.objects.get(id=classroom_id)    
    students = Student.objects.filter(classroom=classroom).order_by('name')
    attendance = Attendance.objects.filter(student__in=students, classroom=classroom, date=today)

    context = {
        "classroom": classroom,        
        "students": students,
        "attendance":attendance,
    }
    return render(request, 'myclassrooms_detail.html', context)   

### STUDENTS ###
def student_create(request, classroom_id):
    form = StudentForm()
    classroom = Classroom.objects.get(id=classroom_id)
    if request.user == classroom.teacher:
        if request.method == "POST":
            form = StudentForm(request.POST)
            if form.is_valid():
                student = form.save(commit=False)
                student.classroom = classroom
                student.save()
                return redirect('my-classrooms-detail', classroom_id)
            print (form.errors)
    context = {
    "form": form,
    "classroom": classroom,
    }
    return render(request, 'create_student.html', context)

def student_update(request, classroom_id, student_id):
    classroom = Classroom.objects.get(id=classroom_id)
    student = Student.objects.get(classroom=classroom, id=student_id)
    if request.user == classroom.teacher:
        form = StudentForm(instance=student)
        if request.method == "POST":
            form = StudentForm(request.POST, instance=student)
            if form.is_valid():
                form.save()
                return redirect('my-classrooms-detail', classroom_id)
            print (form.errors)
    context = {
    "form": form,
    "classroom": classroom,
    "student": student,
    }
    return render(request, 'update_student.html', context)

def student_delete(request, classroom_id, student_id):
    classroom = Classroom.objects.get(id=classroom_id)
    if request.user == classroom.teacher:
        Student.objects.get(classroom=classroom, id=student_id).delete()
        return redirect('my-classrooms-detail', classroom_id)


### ATTENDANCE ### 
def take_attendance(request, classroom_id):
    today = timezone.now().date()
    classroom = Classroom.objects.get(id=classroom_id)
    students = classroom.students.all()
    for student in students:
        Attendance.objects.get_or_create(classroom=classroom, student=student, date=today)
    AttendanceFormSet = modelformset_factory(Attendance, form=AttendanceForm, extra=0)
    qs = Attendance.objects.filter(student__in=students, date=today)
    formset = AttendanceFormSet(queryset=qs)
    if request.method == "POST":
        print(request.POST)
        formset = AttendanceFormSet(request.POST, queryset=qs)
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    form.save()
            formset.save()
            return redirect('my-classrooms-detail', classroom_id)

    context = {
        "classroom": classroom,
        "formset": formset,
    }
    return render(request, "create_attendance.html", context)


### AUTHENTICATION ### 
def signin(request):
    if request.user.is_authenticated:
        return redirect('semester-list')
    form = SigninForm()
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('semester-list')
    context = {
        "form":form
    }
    return render(request, 'signin.html', context)

def signout(request):
    logout(request)
    return redirect('signin')

def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(user.password)
            user.save()

            login(request, user)
            return redirect("semester-list")
    context = {
        "form":form,
    }
    return render(request, 'signup.html', context)