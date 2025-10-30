from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

# forms.py
from django import forms

class MovieFilterForm(forms.Form):
    SORT_CHOICES = [
        ('title', 'По названию (А-Я)'),
        ('year_desc', 'По году (новые)'),
        ('year_asc', 'По году (старые)'),
        ('price_desc', 'По цене (дорогие)'),
        ('price_asc', 'По цене (дешевые)'),
    ]
    
    GENRE_CHOICES = [
        ('', 'Все жанры'),
        ('боевик', 'Боевик'),
        ('комедия', 'Комедия'),
        ('драма', 'Драма'),
        ('фантастика', 'Фантастика'),
        ('ужасы', 'Ужасы'),
        ('триллер', 'Триллер'),
        ('мелодрама', 'Мелодрама'),
        ('приключения', 'Приключения'),
    ]
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите название фильма...',
            'class': 'form-control'
        })
    )
    
    genre = forms.ChoiceField(
        choices=GENRE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    min_year = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'placeholder': '1900',
            'class': 'form-control',
            'min': 1900,
            'max': 2030
        })
    )
    
    max_year = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'placeholder': '2024',
            'class': 'form-control',
            'min': 1900,
            'max': 2030
        })
    )
    
    min_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'placeholder': '0',
            'class': 'form-control',
            'min': 0,
            'step': 10
        })
    )
    
    max_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'placeholder': '5000',
            'class': 'form-control',
            'min': 0,
            'step': 10
        })
    )
    
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        initial='title',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
# форма профиля пользователя
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

#форма покупки фильма
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