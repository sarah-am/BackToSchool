from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .models import Classroom, Student, Attendance, Performance, Test
from .forms import StudentForm, SignupForm, SigninForm, ClassroomForm, AttendanceForm, UploadFileForm, PerformanceForm, TestForm
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q
import csv

### CLASSROOMS ###
def classroom_list(request):
    if request.user.is_anonymous:
        return redirect('signin')
    
    classrooms_list = Classroom.objects.filter(teacher=request.user).order_by('title')
    
    #Search bar (does not work)
    query = request.GET.get('q')
    for classroom in classrooms_list:
        if query: 
            students = classroom.students.filter(classroom=classroom).filter(Q(name__icontains=query)).distinct()

    #Pagination (works)
    page = request.GET.get('page', 1)

    paginator = Paginator(classrooms_list, 3)
    try:
        classrooms = paginator.page(page)
    except PageNotAnInteger:
        classrooms = paginator.page(1)
    except EmptyPage:
        classrooms = paginator.page(paginator.num_pages)

    context = {
        "classrooms": classrooms,
    }
    return render(request, 'classroom_list2.html', context)

def classroom_detail(request, classroom_id):
    if request.user.is_anonymous:
        return redirect('signin')
    classroom = Classroom.objects.get(id=classroom_id, teacher=request.user)    

    context = {
        "classroom": classroom,        
    }
    return render(request, 'classroom_detail.html', context)  

def classroom_create(request):
    if request.user.is_anonymous:
        return redirect('signin')
    form = ClassroomForm()
    if request.method == "POST":
        form = ClassroomForm(request.POST)
        if form.is_valid():
            classroom = form.save(commit=False)
            classroom.teacher = request.user
            classroom.save()
            return redirect('classroom-list')
    
    context = {
        "form": form,
    }
    return render(request, 'create_classroom.html', context)

def classroom_update(request, classroom_id):
    if request.user.is_anonymous:
        return redirect('signin')
    classroom = Classroom.objects.get(id=classroom_id)
    form = ClassroomForm(instance=classroom)
    if request.method == "POST":
        form = ClassroomForm(request.POST, instance=classroom)
        if form.is_valid():
            form.save()
            return redirect('classroom-list')
    context = {
        "form": form,
        "classroom": classroom,
    }
    return render(request, 'update_classroom.html', context)

def classroom_delete(request, classroom_id):
    if request.user == classroom.teacher:
        Classroom.objects.get(id=classroom_id).delete()
        return redirect('classroom-list')


### STUDENTS ###
def student_detail(request, student_id):
    if request.user.is_anonymous:
        return redirect('signin')
    student = Student.objects.get(id=student_id)

    context = {
        'student': student
    }

    return render(request, 'student_detail.html', context)

def student_create(request):
    form = StudentForm()
    if not request.user == classroom.teacher:
        raise HttpResponse("Invalid Authorization")
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            return redirect('classroom-list')
        print (form.errors)
    context = {
        "form": form,
    }
    return render(request, 'create_student.html', context)

def student_update(request, student_id):
    if not request.user == classroom.teacher:
        raise HttpResponse("Invalid Authorization")
    student = Student.objects.get(id=student_id)
    form = StudentForm(instance=student)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('classroom-list')
        print (form.errors)
    context = {
    "form": form,
    "student": student,
    }
    return render(request, 'update_student.html', context)

def student_delete(request, student_id):
    Student.objects.get(id=student_id).delete()
    return redirect('classroom-list')


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
        formset = AttendanceFormSet(request.POST, queryset=qs)
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    form.save()
            formset.save()
            return redirect('classroom-list')

    context = {
        "classroom": classroom,
        "formset": formset,
    }
    return render(request, "create_attendance.html", context)


### PERFORMANCE ### 
def record_performance(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    students = classroom.students.all()
    
    # for student in students:
    #     Performance.objects.get_or_create(classroom=classroom, student=student)

    PerformanceFormSet = modelformset_factory(Performance, form=PerformanceForm, extra=0)
    qs = Performance.objects.filter(student__in=students)
    formset = PerformanceFormSet(queryset=qs)
    
    if request.method == "POST":
        formset = PerformanceFormSet(request.POST, queryset=qs)
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    form.save()
            formset.save()
            return redirect('classroom-list')

    context = {
        "classroom": classroom,
        "formset": formset,
    }
    return render(request, "record_performance2.html", context)

# def record_performance(request):
#     # classroom = Classroom.objects.filter(teacher=request.user)
#     # performance = Performance.objects.filter(id=student_id, classroom=classroom) 
#     form = PerformanceForm()
    
#     if request.method == "POST":
#         form = PerformanceForm(request.POST)
#         if form.is_valid():
#             performance = form.save(commit=False)
#             performance.save()
#             return redirect('classroom-list')

#     context = {
#         # "performance": performance,
#         "form": form,
#     }
#     return render(request, "record_performance.html", context)

def test_create(request):
    form = TestForm()
    if request.method == "POST":
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.save()
            return redirect('classroom-list')
        print (form.errors)
    
    context = {
        "form": form,
    }
    return render(request, 'create_test.html', context)

### UPLOAD/EXPORT ### 
def upload_file(request):
    form = UploadFileForm()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = Attendance(upload=request.FILES['file'])
            instance.save()
            return redirect('classroom-list')

    context = {
        'form': form,
        'attendance':attendance
    }
    return render(request, 'upload.html', context)

def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendances.csv"'

    writer = csv.writer(response)
    writer.writerow(['Classroom ID', 'Classroom', 'Student ID', 'Student', 'Status', 'Date', 'Notes'])

    attendances = Attendance.objects.all().values_list('classroom', 'classroom__title', 'student', 'student__name', 'status', 'date', 'notes') \
        .distinct().order_by('classroom')
    
    for attendance in attendances:
        writer.writerow(attendance)

    return response


### VISUAL DATA ### 
def chart(request):
    return render(request,'chart.html', {'attendance':Attendance.objects.all()})


### AUTHENTICATION ### 
def signin(request):
    if request.user.is_authenticated:
        return redirect('classroom-list')
    form = SigninForm()
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('classroom-list')
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
            return redirect("classroom-list")
    context = {
        "form":form,
    }
    return render(request, 'signup.html', context)