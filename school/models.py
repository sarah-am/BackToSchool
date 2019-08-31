from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User, AbstractUser

class User(AbstractUser):
  USER_TYPE_CHOICES = (
      (1, 'student'),
      (2, 'teacher'),
  )

  user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)

class Teacher(models.Model):
	user = models.OneToOneField(User)

class Course(models.Model):
	name = models.CharField(max_length=120)
	subject = models.CharField(max_length=120)
	year = models.IntegerField()
	teacher = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

class Student(models.Model):
	user = models.OneToOneField(User)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=(('M','Male'), ('F','Female')))
    photo=models.ImageField(upload_to="student",blank=True,null=True)
    exam_grade = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
    	return ("%s, %s, %s, %s") % (Student.name, Student.date_of_birth, Student.gender, Student.exam_grade)

class Attendance(models.Model):
    student = models.ForeignKey(Student)
    date = models.DateField(default=datetime.datetime.now, validators=settings.DATE_VALIDATORS)
    time = models.TimeField(blank=True,null=True)
    notes = models.CharField(max_length=500, blank=True)