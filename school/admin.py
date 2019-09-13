from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Semester, Classroom, Student


# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = User
#     list_display = ('email', 'is_staff', 'is_active',)
#     list_filter = ('email', 'is_staff', 'is_active',)
#     fieldsets = (
#         (None, {'fields': ('name', 'email', 'password')}),
#         ('Permissions', {'fields': ('is_staff', 'is_active')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
#         ),
#     )
#     search_fields = ('email',)
#     ordering = ('email',)

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

