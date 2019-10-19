from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Semester(models.Model):
    season_choices = (
        ('Fall', 'Fall'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
    )
    year = models.PositiveIntegerField()
    season = models.CharField(max_length=6, choices=season_choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['season', 'year'], name='semester')
        ]

    def __str__(self):
        return ("%s, %s") % (self.season, self.year)


class Classroom(models.Model):
    title = models.CharField(max_length=120)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='classrooms')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classrooms')
    # description = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('classroom-list')

    # def avg_grade(request):
    #     return self.performance.aggregate(Avg('grade'))


class Student(models.Model):
    name = models.CharField(max_length=120)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=(('M','Male'), ('F','Female')))
    photo = models.ImageField(upload_to="student", blank=True, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='students')
    email = models.EmailField(max_length=70)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('student-detail', kwargs={'student_id':self.id})
    
    def present(self):
        return self.attendance.filter(status='P').count()

    def absent(self):
        return self.attendance.filter(status='A').count()

    def late(self):
        return self.attendance.filter(status='L').count()

    def calculate_total_gpa(request):
        return sum(self.performance.grade * self.performance.weight) 


class Attendance(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='attendance')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')
    status = models.CharField(max_length=1, choices=(('P','Present'), ('A','Absent'), ('L','Late')), default='A')
    date = models.DateField()
    notes = models.CharField(max_length=500, blank=True)
    upload = models.FileField(upload_to='uploads/%Y/%m/%d/')


class Test(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='tests')
    name = models.CharField(max_length=25)
    weight = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    date = models.DateField()

    def __str__(self):
        return self.name

class Performance(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='performance')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='performance')
    grade = models.PositiveIntegerField(validators=[MaxValueValidator(100),MinValueValidator(0)], null=True)
    weight = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='performance')
    notes = models.CharField(max_length=500, blank=True)
    upload = models.FileField(upload_to='uploads/%Y/%m/%d/')

    def __str__(self):
        return self.student.name

