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

    path('classrooms/', views.classroom_list, name='classroom-list'),
    path('classrooms/create/', views.classroom_create, name='classroom-create'),
    path('classrooms/<int:classroom_id>/', views.classroom_detail, name='classroom-detail'),
    path('classrooms/<int:classroom_id>/update/', views.classroom_update, name='classroom-update'),
    path('classrooms/<int:classroom_id>/delete/', views.classroom_delete, name='classroom-delete'),    
    path('classrooms/<int:classroom_id>/attendance/', views.take_attendance, name='take-attendance'),

    path('students/create', views.student_create, name='student-create'),
    path('students/<int:student_id>/update/', views.student_update, name='student-update'),
    path('students/<int:student_id>/delete/', views.student_delete, name='student-delete'),

    path('upload/', views.upload_file, name='upload-file'),
    path('export/', views.export_attendance_csv, name='export_attendance_csv'),
    path('chart/', views.chart, name='chart'),

]


if settings.DEBUG:
	urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

