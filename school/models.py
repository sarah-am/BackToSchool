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
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='classrooms')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classrooms')
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    date = models.DateField(null=True)
    credits = models.IntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])

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

    # class Meta:
    #     permissions = (("is_student", "is_student"), )


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

    # class Meta:
    #     unique_together = ('classroom', 'student')

    def __str__(self):
        return self.status

    def get_absolute_url(self):
        return reverse('take-attendance', kwargs={'classroom_id':self.id})


    # def get_dates(self):
    #     clasrooms = Classroom.objects.all()


    # def save(self, *args, **kwargs):
    #     """Don't save Present """
    #     present, created = AttendanceStatus.objects.get_or_create(name="Present")
    #     if self.status != present:
    #         super(StudentAttendance, self).save(*args, **kwargs)
    #     else:
    #         try: self.delete()
    #         except: pass


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



# class User(AbstractUser):
#     @property
#     def is_student(self):
#         if hasattr(self, 'student'):
#             return True
#         return False

#     @property
#     def is_teacher(self):
#         if hasattr(self, 'teacher'):
#             return True
#         return False



# from django.contrib.auth import REDIRECT_FIELD_NAME
# from django.contrib.auth.decorators import user_passes_test


# def student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
#     '''
#     Decorator for views that checks that the logged in user is a student,
#     redirects to the log-in page if necessary.
#     '''
#     actual_decorator = user_passes_test(
#         lambda u: u.is_active and u.is_student,
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if function:
#         return actual_decorator(function)
#     return actual_decorator


# def teacher_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
#     '''
#     Decorator for views that checks that the logged in user is a teacher,
#     redirects to the log-in page if necessary.
#     '''
#     actual_decorator = user_passes_test(
#         lambda u: u.is_active and u.is_teacher,
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if function:
#         return actual_decorator(function)
#     return actual_decorator
