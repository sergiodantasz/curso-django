from django.http import Http404
from django.shortcuts import redirect, render

from authors.forms import RegisterForm


def register(request):
    register_form_data = request.session.get('register_form_data')
    form = RegisterForm(register_form_data)
    return render(
        request,
        'authors/pages/register.html',
        {
            'form': form,
        }
    )


def register_create(request):
    if not request.POST:
        raise Http404()
    post = request.POST
    request.session['register_form_data'] = post
    return redirect('authors:register')
    form = RegisterForm(post)
    # return render(
    #     request,
    #     'authors/pages/register.html',
    #     {
    #         'form': form,
    #     }
    # )
