from django.shortcuts import render


def home(request):
    return render(request, 'recipes/home.html', {
        'name': 'Sérgio Dantas',
    })


def about(request):
    return render(request, 'recipes/about.html', {
        'name': 'Sérgio Dantas',
    })
