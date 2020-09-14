"""Assessment_v2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from . import views

urlpatterns = [
    path('home/',views.home, name='home'),
    path('login/', views.login_page , name='login_page'),
    path('admin_panel/',views.admin_panel, name='admin_panel'),
    path('about/',views.about_page, name='about_page'),
    path('contact/',views.contact_page, name='contact_page'),
    path('admin_panel/display_test',views.display_test, name = 'display_test'),
    path('logout', views.logout_request, name="logout"),
    path('admin_panel/create_test/', views.create_test, name='create_test'),
    path('<slug:test_id>/submit', views.submit_response, name='submit'),##########copy link button remain
    path('<slug:test_id>/<slug:grading_id>', views.grading, name='grading'),#########copy link
    path('upload-excel/', views.upload_excel,name='upload_excel'),#""""""
    #path('upload-test-student/', views.upload_test_student,name='upload_test_student'),
]






