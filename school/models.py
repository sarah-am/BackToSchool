from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class Semester(models.Model):
    season_choices = (
        ('Fall', 'Fall'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
    )

    year = models.IntegerField(('year'), default=datetime.date.today().year, validators=[MinValueValidator(2015), MaxValueValidator(datetime.date.today().year+2)])
    season = models.CharField(max_length=6, choices=season_choices)

    class Meta:
        # unique_together = ('season', 'year')
        constraints = [
            models.UniqueConstraint(fields=['season', 'year'], name='semester')
        ]

    def __str__(self):
        return "{}, {}".format(self.season, self.year)

class Classroom(models.Model):
    title = models.CharField(max_length=120)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    # credits = models.

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('classroom-detail', kwargs={'classroom_id':self.id})

class Student(models.Model):
    name = models.CharField(max_length=120)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=(('M','Male'), ('F','Female')))
    photo = models.ImageField(upload_to="student",blank=True,null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    email = models.EmailField(max_length=70, null=True, blank=True, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('student-detail', kwargs={'student_id':self.id})

# class Profile(models.Model):
#     teacher = models.ForeignKey(User, on_delete=models.CASCADE)    
#     classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     # office_hours for teacher


# @receiver(post_save, sender=User)
# def create_profile(sender,instance,**kwargs):
#     if kwargs.get('created', False):
#         Profile.objects.create(user=instance)



# class Performance(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
#     grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
#     weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

# class Attendance(models.Model):
#     classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     status = models.CharField(max_length=1, choices=(('M','Present'), ('F','Absent')))
#     date = models.DateField() #validators=settings.DATE_VALIDATORS)
#     notes = models.CharField(max_length=500, blank=True)

# get or create attendance sheet for the classroom+date
# stick to just teacher sigining in 

#### Finish CRUD by Tues


# class SimpleForm(forms.Form):
#     birth_year = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
#     favorite_colors = forms.MultipleChoiceField(
#         required=False,
#         widget=forms.CheckboxSelectMultiple,
#         choices=FAVORITE_COLORS_CHOICES,
#     )