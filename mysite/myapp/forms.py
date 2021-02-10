from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.forms import ModelForm

from myapp.models import Product, Order, MyUser


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

    # # def __init__(self, *args, **kwargs):
    # #     super().__init__(self, *args, **kwargs)
    # #     self.fields.get('username').label = 'Login'
    # #     self.fields.get('password').label = 'Password'
    #
    # def clean(self):
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')
    #     if not MyUser.objects.filter(username=username).exists():
    #         raise forms.ValidationError(f'Username with login {username} not find')
    #     user = MyUser.objects.filter(username=username).first()
    #     if user:
    #         if not user.check_password(password):
    #             raise forms.ValidationError(f'Incorect password')
    #     return self.cleaned_data

    class Meta:
        model = MyUser
        fields = ['username', 'password']


class RegistrationForm(forms.ModelForm):
    name = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=True)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(self, *args, **kwargs)
    #     self.fields['username'].label = 'Login'
    #     self.fields['password'].label = 'Password'
    #     self.fields['confirm_password'].label = 'confirm_password'
    #     self.fields['name'].label = 'name'
    #     self.fields['email'].label = 'email'

    def clean_email(self):
        email = self.cleaned_data['email']
        if MyUser.objects.filter(email=email).exists():
            raise forms.ValidationError(f'This email has already registration')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if MyUser.objects.filter(username=username).exists():
            raise forms.ValidationError(f'This {username} has already registration')
        return username

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Inncorect password')
        return self.cleaned_data

    class Meta:
        model = MyUser
        fields = ['username', 'name', 'email', 'password', 'confirm_password']


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'description', 'price', 'quantity', 'available']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['costumer', 'product', 'quantity', 'total_price']
