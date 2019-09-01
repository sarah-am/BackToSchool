from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


class Semester(models.Model):
    season_choices = (
        ('FA', 'Fall')
        ('SP', 'Spring')
        ('SM', 'Summer')
        )

    year = models.IntegerField(_('year'), default=datetime.date.today().year, validators=[MinValueValidator(2015), MaxValueValidator(datetime.date.today().year+2)])
    # year = models.DateField(default=datetime.date.today().year)
    season = models.CharField(max_length=6, choices=season_choices)

    def __str__(self):
        return ('%s', "", "%s") % (self.season, self.year)

class Classroom(models.Model):
    title = models.CharField(max_length=120)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

class Student(models.Model):
    name = models.CharField(max_length=120)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=(('M','Male'), ('F','Female')))
    photo = models.ImageField(upload_to="student",blank=True,null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    email = models.EmailField(max_length=70, null=True, blank=True, unique=True)


# class Attendance(models.Model):
#     classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     status = models.CharField(max_length=1, choices=(('M','Present'), ('F','Absent')))
#     date = models.DateField() #validators=settings.DATE_VALIDATORS)
#     notes = models.CharField(max_length=500, blank=True)

# get or create attendance sheet for the classroom+date
# stick to just teacher sigining in 


# class SimpleForm(forms.Form):
#     birth_year = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
#     favorite_colors = forms.MultipleChoiceField(
#         required=False,
#         widget=forms.CheckboxSelectMultiple,
#         choices=FAVORITE_COLORS_CHOICES,
#     )