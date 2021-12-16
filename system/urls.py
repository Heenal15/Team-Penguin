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
    path('', views.homepage_views.homepage, name='homepage'),
    path('dashboard/', views.static_views.home, name='home'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('password/', views.PasswordView.as_view(), name='password'),
    path('unauthorised_access/', views.unauthorised_access, name='unauthorised_access'),
    path('member/<int:user_id>', views.show_member, name='show_member'),
    path('user/<int:user_id>', views.show_user, name='show_user'),
    path('members/', views.member_list, name='member_list'),
    path('member_list_for_officer/', views.member_list_for_officer, name='member_list_for_officer'),
    path('members_and_officers_for_clubowner/', views.members_and_officers_for_clubowner, name='members_and_officers_for_clubowner'),
    path('applicants/', views.applicant_list, name='applicant_list'),
    path('officers/', views.officers, name='officers'),
    #path('approve/<int:user_id>', views.approve, name='approve'),
    #path('unapprove/<int:user_id>', views.unapprove, name='unapprove'),
    #path('promote/<int:user_id>', views.promote, name='promote'),
    #path('demote/<int:user_id>', views.demote, name='demote'),
    #path('make_owner/<int:user_id>', views.make_owner, name='make_owner'),
    path('club_sign_up/', views.club_sign_up, name='club_sign_up'),
    path('club_list/', views.club_list, name='club_list'),
    path('create_club/', views.create_club, name='create_club'),
    path('load_club/', views.load_club, name='load_club'),
]
