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

    # path('courses/', views.course_list, name='course-list'),
    # path('courses/<int:course_id>/', views.course_detail, name='course-detail'),

    # path('courses/create', views.course_create, name='course-create'),
    # path('courses/<int:course_id>/update/', views.course_update, name='course-update'),
    # path('courses/<int:course_id>/delete/', views.course_delete, name='course-delete'),

    # path('signin/', views.signin, name='signin'),
    # path('signout/', views.signout, name='signout'),
    # path('signup/', views.signup, name='signup'),
    
    # path('noaccess/', views.noaccess, name='noaccess'),

    # path('courses/<int:course_id>/add-student/', views.add_student, name='add-student'),
]


if settings.DEBUG:
	urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
