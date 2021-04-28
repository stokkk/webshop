from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import LogInForm, RegisterForm

from django.contrib.auth.models import User

@login_required(login_url="/account/login")
def AccountView(request):
    return render(request, 'account/account.html', context={'user': request.user})


def LogInView(request):
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            client_data = form.cleaned_data
            user = authenticate(username=client_data['login'],
            password=client_data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("account"))
        return render(request, 'account/login.html', context={     # В случае если форма не верна.
            'user': request.user,
            'form': form,
        })
    form = LogInForm()
    return render(request, 'account/login.html', context={      # Первичное отображение формы.
        'user': request.user,
        'form': form
    })


def LogOutView(request):
    logout(request)
    return HttpResponseRedirect("/")


def RegisterView(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # может быть проверка существования юзера в базе.
            # или она может быть в методе clean формы RegisterForm
            client_data = form.cleaned_data
            user = User(
                username=client_data['login'],
                email=client_data['email'],
                password=client_data['password']
            )

            user.save()
            return HttpResponseRedirect(reverse('login'))
        return render(request, 'account/registration.html', context={
            'user': request.user,
            'form': form})
    
    form = RegisterForm()
    return render(request, 'account/registration.html', context={
        'user': request.user,
        'form': form})