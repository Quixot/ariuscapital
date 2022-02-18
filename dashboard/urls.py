from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('current_projects<int:id>', views.current_projects, name='current_projects'),
]