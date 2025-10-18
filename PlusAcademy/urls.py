from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.courses, name='courses'),
    path('add_courses/', views.add_courses, name='add_courses'),
    path('course_detail/<int:course_id>/', views.course_detail, name='course_detail'),
    path('add_lesson/', views.add_lesson, name='add_lesson'),
    path('lesson_detail/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('lesson_attachment/<int:lesson_id>/attachment/', views.lesson_attachment, name='lesson_attachment'),
    path('about/', lambda request: render(request, 'PlusAcademy/about.html'), name='about'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.profile, name='profile'),
    path('login_view/', views.login_view, name='login'),
    path('logout_view/', views.logout_view, name='logout'),
    path('create_user/', views.create_user, name='create_user'),
    path('change_password/', views.change_password, name='change_password'),
    path('reset_password_request/', views.reset_password_request, name='reset_password_request'),
    path('reset_password_confirm/<int:user_id>/', views.reset_password_confirm, name='reset_password_confirm'),
    path('messages_list/', views.messages_list, name='messages_list'),
    path('manage/', views.manage_courses_lessons, name='manage'),

    path('course/update/<int:course_id>/', views.update_course, name='update_course'),
    path('course/delete/<int:course_id>/', views.delete_course, name='delete_course'),

    path('lesson/update/<int:lesson_id>/', views.update_lesson, name='update_lesson'),
    path('lesson/delete/<int:lesson_id>/', views.delete_lesson, name='delete_lesson'),

    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/delete/", views.delete_account, name="delete_account"),
]