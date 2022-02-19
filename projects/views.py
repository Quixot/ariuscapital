from django.shortcuts import render
from .models import Project, Order


def projects(request):
    projects = Project.objects.all()
    context = {
        'title': 'Наши проекты',
        'projects': projects,
        'sign': 'projects',
    }
    return render(request, 'projects/projects.html', context)


def project(request, id):
    project = Project.objects.get(id=id)
    context = {
        'title': project.title,
        'project': project,
        'sign': 'projects',
    }
    return render(request, 'projects/project.html', context)
