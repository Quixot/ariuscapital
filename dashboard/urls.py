from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('wallet', views.wallet, name='wallet'),
    path('invest', views.invest, name='invest'),
    path('sell', views.sell, name='sell'),
    path('verification', views.verification, name='verification'),
]