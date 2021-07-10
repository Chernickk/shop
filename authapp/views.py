from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import ShopUserLoginForm
from .forms import ShopUserRegisterForm
from .forms import ShopUserEditProfileForm


def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            register_form.save()
            return redirect('index')

    register_form = ShopUserRegisterForm()
    context = {
        'register_form': register_form,
        'title': 'Register page'
    }

    return render(request, 'authapp/register.html', context=context)


def login(request):
    if request.method == 'POST':
        login_form = ShopUserLoginForm(data=request.POST)

        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            if user and user.is_active:
                auth.login(request, user)
                next_ = request.POST['next']
                if next_:
                    return redirect(next_)

                return redirect('index')

    login_form = ShopUserLoginForm()
    context = {
        'login_form': login_form,
        'title': 'Login page'
    }

    return render(request, 'authapp/login.html', context=context)


@login_required
def edit(request):
    if request.method == 'POST':
        edit_profile_form = ShopUserEditProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        if edit_profile_form.is_valid():
            edit_profile_form.save()
            return redirect('auth:edit')
    edit_profile_form = ShopUserEditProfileForm(instance=request.user)

    context = {
        'title': 'Edit profile',
        'edit_profile_form': edit_profile_form
    }

    return render(request, 'authapp/edit.html', context=context)


def logout(request):
    auth.logout(request)
    return redirect('index')
