from django.shortcuts import render
from projects.models import Project, Order


def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


def wallet(request):
    projects = Order.objects.filter(user=request.user.id)
    return render(request, 'dashboard/wallet.html', {'projects': projects})


def invest(request):
    projects = Project.objects.all()
    return render(request, 'dashboard/invest.html', {'projects': projects})


def sell(request):
    projects = Order.objects.filter(user=request.user.id)
    return render(request, 'dashboard/sell.html', {'projects': projects})


def verification(request):
    return render(request, 'dashboard/verification.html')
