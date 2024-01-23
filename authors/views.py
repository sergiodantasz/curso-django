from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from authors.forms import LoginForm, RegisterForm


def register(request):
    register_form_data = request.session.get('register_form_data')
    form = RegisterForm(register_form_data)
    return render(
        request,
        'authors/pages/register.html',
        {
            'form': form,
            'form_action': reverse('authors:register_create'),
        }
    )


def register_create(request):
    if not request.POST:
        raise Http404()
    post = request.POST
    request.session['register_form_data'] = post
    form = RegisterForm(post)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(
            request,
            'Your user has been created successfully, please log in.'
        )
        del(request.session['register_form_data'])
        return redirect(reverse('authors:login'))
    return redirect('authors:register')


def login(request):
    form = LoginForm()
    return render(
        request,
        'authors/pages/login.html',
        {
            'form': form,
            'form_action': reverse('authors:login_create'),
        }
    )


def login_create(request):
    if not request.POST:
        raise Http404()
    form = LoginForm(request.POST)
    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )
        if authenticated_user is not None:
            messages.success(request, 'Login successfully.')
            auth_login(request, authenticated_user)
        else:
            messages.error(request, 'Username or password is invalid.')
    else:
        messages.error(request, 'Username or password is invalid.')
    return redirect(reverse('authors:dashboard'))


@login_required(login_url='authors:login', redirect_field_name='next')
def logout(request):
    if not request.POST:
        messages.error(
            request,
            'Invalid logout request.'
        )
        return redirect(reverse('authors:login'))
    if request.POST.get('username') != request.user.username:
        messages.error(
            request,
            'Invalid logout user.'
        )
        return redirect(reverse('authors:login'))
    messages.success(
        request,
        'Logout completed successfully.'
    )
    auth_logout(request)
    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    return render(request, 'authors/pages/dashboard.html')
