"""backtoschool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from school import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signin, name='signin'),

    path('signout/', views.signout, name='signout'),
    path('signup/', views.signup, name='signup'),

    path('semesters/', views.semester_list, name='semester-list'),
    path('semesters/create/', views.semester_create, name='semester-create'),
    path('semesters/<int:semester_id>/update/', views.semester_update, name='semester-update'),

    path('semesters/<int:semester_id>/classrooms/create/', views.classroom_create, name='classroom-create'),
    path('semesters/<int:semester_id>/classrooms/<int:classroom_id>/delete/', views.classroom_delete, name='classroom-delete'),
    
    path('classrooms/<int:classroom_id>/', views.myclasses_detail, name='my-classrooms-detail'),
    path('classrooms/<int:classroom_id>/update/', views.classroom_update, name='classroom-update'),
    path('classrooms/<int:classroom_id>/attendance/', views.take_attendance, name='take-attendance'),

    path('classrooms/<int:classroom_id>/students/create', views.student_create, name='student-create'),
    path('classrooms/<int:classroom_id>/students/<int:student_id>/update/', views.student_update, name='student-update'),
    path('classrooms/<int:classroom_id>/students/<int:student_id>/delete/', views.student_delete, name='student-delete'),
]


if settings.DEBUG:
	urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

