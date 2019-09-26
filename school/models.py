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
        constraints = [
            models.UniqueConstraint(fields=['season', 'year'], name='semester')
        ]

    def __str__(self):
        return "{}, {}".format(self.season, self.year)

    def get_absolute_url(self):
        return reverse('semester-detail', kwargs={'semester_id':self.id})

class Classroom(models.Model):
    title = models.CharField(max_length=120)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='classrooms')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classrooms')
    # start_time = models.TimeField(null=True)
    # end_time = models.TimeField(null=True)
    # date = models.DateField(null=True)
    # credits = models.IntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('classroom-detail', kwargs={'classroom_id':self.id})

class Student(models.Model):
    name = models.CharField(max_length=120)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=(('M','Male'), ('F','Female')))
    photo = models.ImageField(upload_to="student",blank=True,null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='students')
    email = models.EmailField(max_length=70, null=True, blank=True, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('student-detail', kwargs={'student_id':self.id})
                
class Attendance(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='attendance')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')
    status = models.CharField(max_length=1, choices=(('P','Present'), ('A','Absent'), ('L','Late')), default='A')
    date = models.DateField()
    notes = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.status

    def get_absolute_url(self):
        return reverse('take-attendance', kwargs={'attendance_id':self.id})