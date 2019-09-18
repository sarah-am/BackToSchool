from django import forms
from .models import Semester, Classroom, Student, Attendance
from .models import User
from django.forms.models import inlineformset_factory
from django.forms.models import BaseInlineFormSet


# from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = '__all__'

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['title', 'date']

        widgets = {
            'start_time': forms.TimeInput(attrs={'type':'time'}),
            'end_time': forms.TimeInput(attrs={'type':'time'}),
            'date':forms.DateInput(attrs={'type':'date'})
        }
    
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['classroom']

class AttendanceForm(forms.ModelForm):
    # student = 
    class Meta:
        model = Attendance
        fields = '__all__'

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)                       
        self.fields['student'].disabled = True

    # def get_date(self):

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


### FORMSET
# StudentsFormset = inlineformset_factory(models.Classroom, models.Student, extra=1)
# AttendanceFormset = inlineformset_factory(models.Student, models.Attendance, extra=1)

# class BaseChildrenFormset(BaseInlineFormSet):
#     pass



## other formset example:
# class TakeAttendanceForm(forms.ModelForm):

#     class Meta:
#         model = Attendance
#         exclude = ()

# AttendanceFormSet = inlineformset_factory(
#     Student, Attendance, form=TakeAttendanceForm,
#     fields=['name', 'date'], extra=1
#     )


##
# class BaseChildrenFormset(BaseInlineFormSet):

#     def add_fields(self, form, index):
#         super(BaseChildrenFormset, self).add_fields(form, index)

#         # save the formset in the 'nested' property
#         form.nested = AttendanceFormset(
#                         instance=form.instance,
#                         data=form.data if form.is_bound else None,
#                         files=form.files if form.is_bound else None,
#                         )

#     def is_valid(self):
#         result = super(BaseChildrenFormset, self).is_valid()

#         if self.is_bound:
#             for form in self.forms:
#                 if hasattr(form, 'nested'):
#                     result = result and form.nested.is_valid()

#         return result

#     def save(self, commit=True):

#         result = super(BaseChildrenFormset, self).save(commit=commit)

#         for form in self.forms:
#             if hasattr(form, 'nested'):
#                 if not self._should_delete_form(form):
#                     form.nested.save(commit=commit)

#         return result

# def student_count(self, id):
#     classroom = Classroom.objects.get(id=classroom_id)
#     students = Student.objects.get(instance=classroom)

#     for student in students:
#         student.count()

# AttendanceFormset = inlineformset_factory(Classroom, Attendance, formset=BaseChildrenFormset, exclude=(), extra=1)











# ValueError: 'school.Student' has no ForeignKey to 'school.Attendance'.

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