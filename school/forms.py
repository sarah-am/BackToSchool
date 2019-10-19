from django import forms
from .models import Semester, Classroom, Student, Attendance, Performance, Test
from .models import User


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = '__all__'


class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        exclude = ['teacher']

    
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = '__all__'

        widgets = {
            'dob':forms.DateInput(attrs={'type':'date'})
        }


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        exclude = ['classroom', 'date', 'student', 'upload']

        widgets = {
            'notes': forms.Textarea(attrs={'rows':"1", 'cols':"25"})
        }


class PerformanceForm(forms.ModelForm):
    class Meta:
        model = Performance
        exclude = ['classroom', 'student', 'upload']

        widgets = {
            'notes': forms.Textarea(attrs={'rows':"1", 'cols':"25"})
        }


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = '__all__'
    
        widgets = {
            'date':forms.DateInput(attrs={'type':'date'})
        }
        

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ,'password']

        widgets={
        'password': forms.PasswordInput(),
        }


class SigninForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

