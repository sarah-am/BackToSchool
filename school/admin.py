from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Teacher, Course, Student, Attendance


# Register your models here.
admin.site.register(User, UserAdmin)