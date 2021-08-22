import logging
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from .models import ShopUser
from .forms import ShopUserLoginForm
from .forms import ShopUserRegisterForm
from .forms import ShopUserEditForm
from .forms import ShopUserEditProfileForm

logger = logging.getLogger(__name__)


def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            if send_verify_mail(user):
                logger.info(f'message sended to user {user.email}')
            else:
                logger.error(f'error sending message to user {user.email}')
            return redirect('index')
    else:
        register_form = ShopUserRegisterForm()
    context = {
        'register_form': register_form,
        'title': 'Register page',
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
                next_ = request.POST.get('next')
                if next_:
                    return redirect(next_)

                return redirect('index')
    else:
        login_form = ShopUserLoginForm()
    context = {
        'login_form': login_form,
        'title': 'Login page'
    }

    return render(request, 'authapp/login.html', context=context)


@login_required
def edit(request):
    if request.method == 'POST':
        edit_form = ShopUserEditForm(data=request.POST, files=request.FILES, instance=request.user)
        edit_profile_form = ShopUserEditProfileForm(data=request.POST, instance=request.user.shopuserprofile)
        if edit_profile_form.is_valid() and edit_form.is_valid():
            edit_profile_form.save()
            edit_form.save()
            return redirect('auth:edit')
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        edit_profile_form = ShopUserEditProfileForm(instance=request.user.shopuserprofile)

    context = {
        'title': 'Edit profile',
        'edit_form': edit_form,
        'edit_profile_form': edit_profile_form,
    }

    return render(request, 'authapp/edit.html', context=context)


def logout(request):
    auth.logout(request)
    return redirect('index')


def verify(request, email, activation_key):
    try:
        status = False
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and user.is_activation_key_valid():
            user.is_active = True
            user.save()
            auth.login(request, user)
            status = True
        else:
            logger.error(f'error activating user with email {email}')
    except Exception as e:
        logger.error(f'error activating user with {email} args: {e}')
    finally:
        context = {
            'title': 'Активация аккаунта',
            'status': status
        }
        
        return render(request, 'authapp/verify.html', context=context)


def send_verify_mail(user):
    verify_link = reverse('auth:verify', kwargs={
        'email': user.email,
        'activation_key': user.activation_key
    })
    title = f'Активация аккаунта {user.username}'
    message = f'Для активации вашего аккаунта перейдите по ссылке {settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
