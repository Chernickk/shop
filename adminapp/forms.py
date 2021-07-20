from django import forms
from authapp.models import ShopUser
from authapp.forms import ShopUserRegisterForm
from authapp.forms import ShopUserEditProfileForm
from mainapp.models import ProductCategory


class ShopUserAdminRegisterForm(ShopUserRegisterForm):
    date_of_birth = forms.DateField(required=False)
    image = forms.ImageField(required=False)
    is_staff = forms.BooleanField(required=False)

    class Meta:
        model = ShopUser
        fields = ['username',
                  'first_name',
                  'last_name',
                  'password1',
                  'password2',
                  'email',
                  'date_of_birth',
                  'image',
                  'is_staff']


class ShopUserAdminEditProfileForm(ShopUserEditProfileForm):
    date_of_birth = forms.DateField(required=False)
    image = forms.ImageField(required=False)
    is_staff = forms.BooleanField(required=False)
    is_superuser = forms.BooleanField(required=False)

    class Meta:
        model = ShopUser
        fields = ['username',
                  'first_name',
                  'last_name',
                  'password',
                  'email',
                  'date_of_birth',
                  'image',
                  'is_staff',
                  'is_superuser']


class CategoryCreateForm(forms.ModelForm):
    is_deleted = forms.BooleanField(required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = ProductCategory
        fields = ('name', 'description')


class CategoryEditForm(forms.ModelForm):
    is_deleted = forms.BooleanField(required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = ProductCategory
        fields = ('name', 'description', 'is_deleted')
