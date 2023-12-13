from django.contrib import messages
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
    form = RegisterForm(post)
    if form.is_valid():
        form.save()
        messages.success(
            request,
            'Your user has been created successfully, please log in.'
        )
        del(request.session['register_form_data'])
    return redirect('authors:register')
    # return render(
    #     request,
    #     'authors/pages/register.html',
    #     {
    #         'form': form,
    #     }
    # )
