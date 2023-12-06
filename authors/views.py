from django.shortcuts import render


def register(request):
    return render(
        request,
        'authors/pages/register.html',
    )
