from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from calorie.apps.user.forms import UserCreateForm


def register(request):
    if request.POST:
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            account = authenticate(email=user.email, password=form.cleaned_data.get('password1'))
            login(request, account)
            return redirect('home')
    else:
        form = UserCreateForm()
    return render(request, 'registration/register.html', context={
        'form': form
    })
