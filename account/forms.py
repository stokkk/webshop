from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import string
from main.models import Country

class LogInForm(forms.Form):
    login = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control form-account',}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-account',}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].label = "Ваш логин"
        self.fields['password'].label = "Ваш пароль"
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('login')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Неверный логин или пароль.")
        return cleaned_data    
            
    def clean_login(self):
        login = self.cleaned_data['login']
        if login[0] in string.punctuation + string.digits + string.whitespace:
            raise ValidationError("Логин должен начинаться с латинской буквы.")
        if len(login) > len(login.replace(' ', '')):
            raise ValidationError("Логин не должен содержать пробелов и знаков табуляции.")
        if login.isnumeric():
            raise ValidationError("Логин не может состоять только из цифр.")
        return login
    
    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) > len(password.replace(' ', '')):
            raise ValidationError("Пароль не должен содержать пробелов и знаков табуляции.")
        if len(password) < 3:
            raise ValidationError("Пароль должен состоять из 3 и более символов")
        return password
    class Meta:
        model = User
        fields = ['login', 'password']


class RegisterForm(forms.Form):
    login = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-account',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control form-account',
        'placeholder': 'example@email.com'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-account',
    }))

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким E-mail адресом уже существует в системе.")
        return email
    
    def clean_login(self):
        login = self.cleaned_data['login']
        if login[0] in string.punctuation + string.digits + string.whitespace:
            raise ValidationError("Логин должен начинаться с латинской буквы.")
        if len(login) > len(login.replace(' ', '')):
            raise ValidationError("Логин не должен содержать пробелов и знаков табуляции.")
        if login.isnumeric():
            raise ValidationError("Логин не может состоять только из цифр.")
        if User.objects.filter(username=login).exists():
            raise ValidationError("Пользователь с таким логином уже есть в системе.")
        return login
    
    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) > len(password.replace(' ', '')):
            raise ValidationError("Пароль не должен содержать пробелов и знаков табуляции.")
        if len(password) < 3:
            raise ValidationError("Пароль должен состоять из 3 и более символов")
        return password


class OrderForm(forms.Form):
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={'class': 'district', }
    ))
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={'class': 'district', }
    ))
    phone = forms.CharField(max_length=10, widget=forms.TextInput(
        attrs={'class': 'district', }
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'district', }
    ))
    country = forms.ChoiceField(choices=Country.get_countries(), widget=forms.Select(
        attrs={'class': 'district', }
    ))
    street = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'district', }
    ))
    city = forms.CharField(max_length=25, widget=forms.TextInput(
        attrs={'class': 'district', }
    ))
    postcode = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={'class': 'district', }
    ))
    comment = forms.CharField(max_length=500, widget=forms.TextInput(
        attrs={'class': 'district', }
    ))

    