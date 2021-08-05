from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.forms import PasswordInput, ModelForm, CharField
from uuid import uuid4
from hashlib import sha1
from .models import ShopUser, ShopUserProfile


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ShopUserRegisterForm(UserCreationForm):
    date_of_birth = forms.DateField(required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'password1', 'password2', 'email', 'date_of_birth', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_staff':
                field.widget.attrs['class'] = 'form-control'
                field.help_text = ''

    def save(self, commit=True):
        user = super().save()

        try:
            user.is_active = False
            salt = str(uuid4())[:8]
            user.activation_key = sha1(f'{user.email}{salt}'.encode()).hexdigest()
            user.save()
        except Exception as e:
            user.delete()

        return user


class ShopUserEditForm(ModelForm):
    password = CharField(widget=PasswordInput, required=False)

    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'email', 'date_of_birth', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['is_staff', 'is_superuser', 'is_deleted']:
                field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ShopUserEditProfileForm(ModelForm):
    class Meta:
        model = ShopUserProfile
        fields = ('tagline', 'about', 'gender',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # if field_name not in ['is_staff', 'is_superuser', 'is_deleted']:
            field.widget.attrs['class'] = 'form-control'


