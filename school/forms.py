from django import forms
from .models import Course, Student
from django.contrib.auth.models import User

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['course','date_of_birth']

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