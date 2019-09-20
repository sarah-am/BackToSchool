from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import Semester, Classroom, Student, Attendance
from .forms import StudentForm, SignupForm, SigninForm, SemesterForm, ClassroomForm, AttendanceForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import modelformset_factory, inlineformset_factory
from django.utils import timezone


###test
def test(request):
    pass

    return render(request, 'dashboard.html')

### SEMESTERS ###
def semester_list(request):
    semesters = Semester.objects.all().order_by('year')
    classrooms = Classroom.objects.filter(semester__in=semesters).order_by('title')
    query = request.GET.get('q')
    if query:
        semesters = semesters.filter(
            Q(season__icontains=query)|
            Q(year__icontains=query)
        ).distinct()

    context = {
        "semesters": semesters,
        "classrooms": classrooms,
    }
    return render(request, 'semester_list.html', context)

def semester_detail(request, semester_id):
    semester = Semester.objects.get(id=semester_id)
    classrooms = Classroom.objects.filter(semester=semester).order_by('title')
    context = {
        "semester": semester,
        "classrooms": classrooms,
    }
    return render(request, 'semester_detail.html', context)

def semester_create(request):
    if request.user.is_anonymous:
        messages.error(request, "Please sign in to create a new semester")
        return redirect('signin')
    form = SemesterForm()
    if request.method == "POST":
        form = SemesterForm(request.POST, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Semester Successfully Created!")
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
                messages.success(request, "Successfully Edited!")
                return redirect('semester-list')
            print (form.errors)
    context = {
    "form": form,
    "semester": semester,
    }
    return render(request, 'update_semester.html', context)


### CLASSROOMS ###
def classroom_list(request):
    classrooms = Classroom.objects.all().order_by('title')
    query = request.GET.get('q')
    if query:
        classrooms = classrooms.filter(
            Q(title__icontains=query)|
            Q(semester__icontains=query)|
            Q(teacher__icontains=query)
        ).distinct()
    
    myclasses_list = []
    if request.user.is_authenticated:
        myclasses_list = request.user.classroom_set.all().values_list('my classes', flat=True)        

    context = {
        "classrooms": classrooms,
        "myclasses_list": myclasses_list,
    }
    return render(request, 'classroom_list.html', context)

def classroom_detail(request, semester_id, classroom_id):
    semester = Semester.objects.get(id=semester_id)
    classroom = Classroom.objects.get(semester=semester, id=classroom_id)    
    # classroom = Classroom.objects.filter(semester=semester)
    students = Student.objects.filter(classroom=classroom).order_by('name')
    context = {
        "semester": semester,
        "classroom": classroom,
        "students": students,
    }
    return render(request, 'classroom_detail.html', context)

def classroom_create(request, semester_id):
    form = ClassroomForm()
    semester = Semester.objects.get(id=semester_id)
    if request.user.is_authenticated: #change to request.user == classroom.teacher later
        if request.method == "POST":
            form = ClassroomForm(request.POST)
            # sub_form = SemesterForm(request.POST)
            if form.is_valid():
                classroom = form.save(commit=False)
                classroom.semester = semester
                classroom.teacher = request.user
                # classroom.semester = sub_form.save()
                classroom.save()
                messages.success(request, "Classroom Successfully Created!")
                return redirect('semester-detail', semester_id)
            print (form.errors)
    context = {
        "form": form,
        "semester": semester,
    }
    return render(request, 'create_classroom.html', context)

def classroom_update(request, semester_id, classroom_id):
    semester = Semester.objects.get(id=semester_id)
    classroom = Classroom.objects.get(semester=semester, id=classroom_id)
    if request.user.is_authenticated:
        form = ClassroomForm(instance=classroom)
        if request.method == "POST":
            form = ClassroomForm(request.POST, instance=classroom)
            if form.is_valid():
                form.save()
                messages.success(request, "Successfully Edited!")
                return redirect('semester-detail', semester_id)
            print (form.errors)
    context = {
    "form": form,
    "semester": semester,
    "classroom": classroom,
    }
    return render(request, 'update_classroom.html', context)

def classroom_delete(request, semester_id, classroom_id):
    Semester.objects.get(id=semester_id)
    if request.user.is_authenticated:
        Classroom.objects.get(id=classroom_id).delete()
        messages.success(request, "Successfully Deleted!")
        return redirect('semester-detail', semester_id)

#### Teacher ####
def myclasses_list(request):
    classrooms = Classroom.objects.filter(pk = request.user.pk)
    # students = Student.objects.filter(user=user) 

    context = {
        "classrooms": classrooms,        
        # "students": students,
    }
    return render(request, 'classroom_list.html', context)

def myclasses_detail(request, classroom_id):
    # classrooms = Classroom.objects.filter(pk = request.user.pk)
    classroom = Classroom.objects.get(id=classroom_id)    
    students = Student.objects.filter(classroom=classroom).order_by('name')

    context = {
        "classroom": classroom,        
        "students": students,
    }
    return render(request, 'myclassrooms_detail.html', context)   

### STUDENTS
def student_create(request, semester_id, classroom_id):
    form = StudentForm()
    semester = Semester.objects.get(id=semester_id)
    classroom = Classroom.objects.get(semester=semester, id=classroom_id)
    if request.user == classroom.teacher:
        if request.method == "POST":
            form = StudentForm(request.POST)
            if form.is_valid():
                student = form.save(commit=False)
                student.classroom = classroom
                student.save()
                messages.success(request, "Student Successfully Added!")
                return redirect('classroom-detail', semester_id, classroom_id)
            print (form.errors)
    context = {
    "form": form,
    "semester": semester,
    "classroom": classroom,
    }
    return render(request, 'create_student.html', context)

def student_update(request, semester_id, classroom_id, student_id):
    semester = Semester.objects.get(id=semester_id)
    classroom = Classroom.objects.get(semester=semester, id=classroom_id)
    student = Student.objects.get(classroom=classroom, id=student_id)
    if request.user == classroom.teacher:
        form = StudentForm(instance=student)
        if request.method == "POST":
            form = StudentForm(request.POST, instance=student)
            if form.is_valid():
                form.save()
                messages.success(request, "Student Successfully Edited!")
                return redirect('classroom-detail', semester_id, classroom_id)
            print (form.errors)
    context = {
    "form": form,
    "semester": semester,
    "classroom": classroom,
    "student": student,
    }
    return render(request, 'update_student.html', context)

def student_delete(request, semester_id, classroom_id, student_id):
    semester = Semester.objects.get(id=semester_id)
    classroom = Classroom.objects.get(semester=semester, id=classroom_id)
    if request.user == classroom.teacher:
        Student.objects.get(classroom=classroom, id=student_id).delete()
        messages.success(request, "Student Successfully Deleted!")
        return redirect('classroom-detail', semester_id, classroom_id)

def mystudents_list(request):
    students = Student.objects.all().order_by('name')
    query = request.GET.get('q')
    if query:
        students = students.filter(
            Q(name__icontains=query)|
            Q(dob__icontains=query)|
            Q(gender__icontains=query)|
            Q(email__icontains=query)
        ).distinct()

    context = {
        "students": students,   
    }
    return render(request, 'student_list.html', context)

### ATTENDANCE ### 
def take_attendance(request, classroom_id):
    today = timezone.now().date()
    classroom = Classroom.objects.get(id=classroom_id)
    students = classroom.students.all()
    for student in students:
        Attendance.objects.get_or_create(classroom=classroom, student=student, date=today)
    AttendanceFormSet = modelformset_factory(Attendance, form=AttendanceForm, extra=0)
    formset = AttendanceFormSet(queryset=Attendance.objects.filter(student__in=students))
    if request.method == "POST":
        pass

        # formset = AttendanceFormSet(request.POST, queryset=Attendance.objects.filter(student__in=students))
        # if formset.is_valid():
        #     formset.save()
        #     messages.success(request, "Attendance taken!")
        # return redirect('my-classrooms-list')

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