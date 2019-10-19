from django.contrib import admin
from .models import Semester, Classroom, Student, Attendance


class ClassroomInline(admin.StackedInline):
	model = Classroom


class SemesterAdmin(admin.ModelAdmin):
	inlines = [ClassroomInline,]


class StudentInline(admin.StackedInline):
	model = Student


class ClassroomAdmin(admin.ModelAdmin):
	inlines = [StudentInline,]


admin.site.register(Semester, SemesterAdmin)
admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(Student)
admin.site.register(Attendance)

