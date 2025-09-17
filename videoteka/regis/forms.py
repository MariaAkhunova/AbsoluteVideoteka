# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

class UserEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        labels = {
            'email': 'Электронная почта'
        }
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваш email'
            })
        }

class PurchaseForm(forms.Form):
    email = forms.EmailField(
        label='Электронная почта для подтверждения',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email'
        })
    )
    confirm = forms.BooleanField(
        label='Я подтверждаю покупку',
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )