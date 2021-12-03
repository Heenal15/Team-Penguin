"""system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from clubs import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('log_in/', views.log_in, name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('register/', views.register, name='register'),
    path('member/<int:user_id>', views.show_member, name='show_member'),
    path('user/<int:user_id>', views.show_user, name='show_user'),
    path('members/', views.member_list, name='member_list'),
    path('member_list_for_officer/', views.member_list_for_officer, name='member_list_for_officer'),
    path('members_and_officers_for_clubowner/', views.members_and_officers_for_clubowner, name='members_and_officers_for_clubowner'),
    path('applicants/', views.applicant_list, name='applicant_list'),
    path('profile/', views.profile, name='profile'),
    path('password/', views.password, name='password'),
    path('waiting_list/', views.waiting_list, name='waiting_list')
]
