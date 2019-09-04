from django import forms
from .models import Semester, Classroom, Student
from .models import User
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = '__all__'

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        exclude = ['teacher']

        widgets={
        'password': forms.PasswordInput(),
        }
        

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['classroom']

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

# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm):
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email' ,'password']

#         widgets={
#         'password': forms.PasswordInput(),
#         }

# class CustomUserChangeForm(UserChangeForm):
#     class Meta(UserChangeForm):
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email' ,'password']