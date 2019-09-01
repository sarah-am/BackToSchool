from django import forms
from .models import Classroom, Student
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CourseForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = '__all__'

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['classroom','date_of_birth']

# class SignupForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email' ,'password']

#         widgets={
#         'password': forms.PasswordInput(),
#         }

class SigninForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ,'password']

        widgets={
        'password': forms.PasswordInput(),
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ,'password']