from django import forms
from .models import Semester, Classroom, Student, Attendance
from .models import User

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = '__all__'

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        exclude = ['semester', 'teacher']

        widgets = {
            'start_time': forms.TimeInput(attrs={'type':'time'}),
            'end_time': forms.TimeInput(attrs={'type':'time'}),
            'date':forms.DateInput(attrs={'type':'date'})
        }
    
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['classroom']

        widgets = {
            'dob':forms.DateInput(attrs={'type':'date'})
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        exclude = ['classroom', 'date', 'student']

        widgets = {
            # 'status': forms.RadioSelect(attrs={'class': "custom-control custom-radio custom-control-inline", 'type':'radio'}),
            # 'student': forms.TextInput(attrs={'readonly class':'form-control-plaintext'}),
            'notes': forms.Textarea(attrs={'rows':"1", 'cols':"25"})
        }

    # def __init__(self, *args, **kwargs): 
    #     super().__init__(*args, **kwargs)                       
    #     self.fields['student'].disabled = True

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