from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('how-it-works', views.how_it_works, name='how-it-works'),
    path('about', views.about, name='about'),
    path('community', views.community, name='community'),
    path('contacts', views.contacts, name='contacts'),
    path('search/', views.search, name='search'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
    path('agreement', views.agreement, name='agreement'),
    path('ajax_projects', views.ajax_projects, name='ajax_projects'),
]