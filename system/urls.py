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
from clubs.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage_view.homepage, name='homepage'),
    path('dashboard/', homepage_view.dashboard, name='dashboard'),
    path('profile/', homepage_view.profile, name='profile'),
    path('log_in/', authentication_view.log_in, name='log_in'),
    path('log_out/', authentication_view.log_out, name='log_out'),
    path('register/', authentication_view.register, name='register'),
    path('password/', authentication_view.password, name='password'),
    path('unauthorised_access/', authentication_view.unauthorised_access, name='unauthorised_access'),
    path('member/<int:user_id>', list_user_view.show_member, name='show_member'),
    path('user/<int:user_id>', list_user_view.show_user, name='show_user'),
    path('members/', list_user_view.member_list, name='member_list'),
    path('member_list_for_officer/', list_user_view.member_list_for_officer, name='member_list_for_officer'),
    path('members_and_officers_for_clubowner/', list_user_view.members_and_officers_for_clubowner, name='members_and_officers_for_clubowner'),
    path('applicants/', list_user_view.applicant_list, name='applicant_list'),
    path('officers/', list_user_view.officers, name='officers'),
    path('approve/<int:user_id>', user_type_change_view.approve, name='approve'),
    path('unapprove/<int:user_id>', user_type_change_view.unapprove, name='unapprove'),
    path('promote/<int:user_id>', user_type_change_view.promote, name='promote'),
    path('demote/<int:user_id>', user_type_change_view.demote, name='demote'),
    path('make_owner/<int:user_id>', user_type_change_view.make_owner, name='make_owner'),
    path('club_sign_up/', club_view.club_sign_up, name='club_sign_up'),
    path('club_list/', club_view.club_list, name='club_list'),
    path('create_club/', club_view.create_club, name='create_club'),
    path('load_club/', club_view.load_club, name='load_club'),
]
