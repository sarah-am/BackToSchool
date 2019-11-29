from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .models import Classroom, Student, Attendance
from .forms import StudentForm, SignupForm, SigninForm, ClassroomForm, AttendanceForm, UploadFileForm
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
import csv

### CLASSROOMS ###
def classroom_list(request):
    if request.user.is_anonymous:
        return redirect('signin')
    
    classrooms_list = Classroom.objects.filter(teacher=request.user).order_by('title')

    page = request.GET.get('page', 1)

    paginator = Paginator(classrooms_list, 20)
    try:
        classrooms = paginator.page(page)
    except PageNotAnInteger:
        classrooms = paginator.page(1)
    except EmptyPage:
        classrooms = paginator.page(paginator.num_pages)

    context = {
        "classrooms": classrooms,
    }
    return render(request, 'classroom_list.html', context)


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
    classroom = Classroom.objects.get(id=classroom_id)
    if request.user == classroom.teacher:
        classroom.delete()
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
    if request.user.is_anonymous:
        return redirect('signin')
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            return redirect('classroom-list')
    context = {
        "form": form,
    }
    return render(request, 'create_student.html', context)

def student_update(request, classroom_id, student_id):
    classroom = Classroom.objects.get(id=classroom_id)
    if not request.user == classroom.teacher:
        raise HttpResponse("Invalid Authorization")
    student = classroom.students.get(id=student_id)
    form = StudentForm(instance=student)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('classroom-list')
    context = {
    "form": form,
    "student": student,
    "classroom":classroom
    }
    return render(request, 'update_student.html', context)

def student_delete(request, student_id):
    Student.objects.get(id=student_id).delete()
    return redirect('classroom-list')


### ATTENDANCE ### 
def detail_and_attendance(request, classroom_id):
    if request.user.is_anonymous:
        return redirect('signin')
    today = timezone.now().date()
    classroom = Classroom.objects.get(id=classroom_id, teacher=request.user)
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
            

    context = {
        "classroom": classroom,
        "formset": formset,
        "students":students

    }
    return render(request, "classroom_detail.html", context)


def update_attendance(request, classroom_id, date):
    attendance = Attendance.objects.filter(classroom_id=classroom_id, date=date)
    
    AttendanceFormSet = modelformset_factory(Attendance, form=AttendanceForm, extra=0)
    formset = AttendanceFormSet(queryset=attendance) #queryset or instance?
    
    if request.method == "POST":
        formset = AttendanceFormSet(request.POST, queryset=attendance)
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    form.save()
            formset.save()
            return redirect('classroom-list')

    context = {
        "classroom_id": classroom_id,
        "formset": formset,
    }
    return render(request, "update_attendance.html", context)


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


def upload_file(request):
    if request.user.is_anonymous:
        return redirect("signin")
    # if not request.user == classroom.teacher:
    #     raise HttpResponse("Invalid Authorization")
    context = {}
    form = UploadFileForm()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            with open('file.txt', 'wb+') as destination: # play around with this; with csv file try to figure out the what kind you need 'file.txt' & 'wb+''
                for chunk in f.chunks():
                    destination.write(chunk)
            csv_file = open('file.txt','r')
            reader = csv.DictReader(csv_file)
            for row in reader:
                # loops through to check if it already exists
                try:
                    new_student, created = Student.objects.get_or_create(name = row['name']) #clean up this part, might not need a try/except
                except Exception:
                    new_student, created = Student.objects.get_or_create(name = row['\ufeffname']) #clean up
                # fill out fields in the model
                new_student.name = row['name']
                new_student.dob = row['dob']
                new_student.gender = row['gender']
                new_student.email = row['email']                
                new_student.classroom = Classroom.objects.get(short_name=row['classroom'])
                new_student.save()
            return render(request, 'upload.html', context)
        else:
            print("form is not valid")
    else:
        context['form'] = form
    return render(request, 'upload.html', context)

# fix this
# def upload_ongoing_file(request):
# #     if not request.user.is_authenticated():
# #         return redirect("/admin")
# # ​
# #     if not request.user.is_staff:
# #         return redirect("/admin")
#     context = {}
#     form = UploadFileForm()
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             f = request.FILES['file']
#             with open('file.txt', 'wb+') as destination: # play around with this; with csv file try to figure out the what kind you need 'file.txt' & 'wb+''
#                 for chunk in f.chunks():
#                     destination.write(chunk)
#             csv_file = open('file.txt','r')
#             reader = csv.DictReader(csv_file)
#             for row in reader:
#                 # loops through to check if it already exists
#                 try:
#                     new_student, created = Student.objects.get_or_create(name = row['name']) #clean up this part, might not need a try/except
#                 except Exception:
#                     new_student, created = Student.objects.get_or_create(name = row['\ufeffname']) #clean up
#                 # fill out fields in the model
#                 new_student.name = row['name']
#                 new_student.dob = row['dob']
#                 new_student.gender = row['gender']
#                 new_student.email = row['email']                
#                 new_student.classroom = Classroom.objects.get(short_name=row['classroom'])
#                 new_student.save()
#             return render(request, 'upload.html', context)
#         else:
#             print("form is not valid")
#     else:
#         context['form'] = form
#     return render(request, 'upload.html', context)

    # should I upload attendance or just the student details???

def export_attendance_csv(request):
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
    return render(request,'chart.html', {'attendance': Attendance.objects.all()})

### 404 Page ### 
def error_404(request):
        context = {}
        return render(request,'404.html', context)

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

## need to adjust signup
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