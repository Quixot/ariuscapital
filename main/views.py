from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from projects.models import Project


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    projects = Project.objects.all()
    context = {
        'title': 'Arius Capital - Платформа коллективных инвестиций',
        'projects': projects,
    }
    return render(request, 'main/index.html', context)


def how_it_works(request):
    context = {
        'title': 'Как это работает',
        'sign': 'howitworks',
    }
    return render(request, 'main/how_it_works.html', context)


def community(request):
    context = {
        'title': 'Сообщество',
        'sign': 'community',
    }
    return render(request, 'main/community.html', context)


def about(request):
    context = {
        'title': 'О компании',
        'sign': 'about',
    }
    return render(request, 'main/about.html', context)


def contacts(request):
    context = {
        'title': 'Контакты',
        'sign': 'contacts',
    }
    return render(request, 'main/contacts.html', context)


def search(request):
    if request.method == 'GET':
        # todos = Todo.objects.filter(description__icontains=request.GET['q'])
        projects = Project.objects.filter(
            Q(title__icontains=request.GET['q']) | Q(deal_sence__icontains=request.GET['q']) | Q(
                deal_why__icontains=request.GET['q']))
    context = {
        'projects': projects,
        'title': 'Search',
    }
    return render(request, 'main/search.html', context)


def privacy_policy(request):
    context = {
        'title': 'Политика конфиденциальности',
    }
    return render(request, 'main/privacy-policy.html', context)


def agreement(request):
    context = {
        'title': 'Договор публичной оферты',
    }
    return render(request, 'main/agreement.html', context)


# Filter Data
def ajax_projects(request):
    projects = Project.objects.all()
    t = render_to_string('main/ajax_projects.html', {'data': projects})
    return JsonResponse({'data': t})
