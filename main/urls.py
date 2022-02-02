from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('how-it-works', views.how_it_works, name='how-it-works'),
    path('about', views.about, name='about'),
    path('community', views.community, name='community'),
    path('contacts', views.contacts, name='contacts'),
    path('search/', views.search, name='search'),
]