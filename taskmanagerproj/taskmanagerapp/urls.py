from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('signout/', views.signout_view, name='signout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add-task/', views.add_task_view, name='add_task'),
    path('task/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('task/edit/<int:task_id>/', views.edit_task, name='edit_task'),
]
