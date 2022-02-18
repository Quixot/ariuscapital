from django.shortcuts import render
from projects.models import Project, Order


def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


def current_projects(request, id):
    projects = Project.objects.filter(type=id)
    return render(request, 'dashboard/projects.html', {'projects': projects})