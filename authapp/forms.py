from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.forms import PasswordInput, ModelForm, CharField
from .models import ShopUser


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'password1', 'password2', 'email', 'date_of_birth', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_staff':
                field.widget.attrs['class'] = 'form-control'
                field.help_text = ''


class ShopUserEditProfileForm(ModelForm):
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



