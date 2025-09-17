# views.py
from django.shortcuts import render, redirect,  get_object_or_404
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Sale, MovieCrew, Movie, Artist, Role
from datetime import date
from .forms import UserEmailForm, PurchaseForm

@login_required
def purchase_movie(request, movie_id):
    movie = get_object_or_404(Movie, movie_id=movie_id)
    user = request.user
    
    # Проверяем, не куплен ли уже фильм
    if Sale.objects.filter(user=user, movie=movie).exists():
        messages.warning(request, f'Фильм "{movie.title}" уже куплен!')
        return redirect('movie_detail', movie_id=movie_id)
    
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # Обновляем email пользователя если он изменился
            if user.email != email:
                user.email = email
                user.save()
                messages.info(request, 'Email успешно обновлен!')
            
            # Создаем запись о покупке
            sale = Sale.objects.create(
                user=user,
                movie=movie,
                unit_price=movie.price
            )
            
            messages.success(request, f'Фильм "{movie.title}" успешно куплен!')
            return redirect('profile')
    else:
        # Предзаполняем текущий email пользователя
        initial_email = user.email if user.email else ''
        form = PurchaseForm(initial={'email': initial_email})
    
    context = {
        'movie': movie,
        'form': form,
    }
    return render(request, 'purchase.html', context)

@login_required
def profile(request):
    user = request.user
    purchases = Sale.objects.filter(user=user).select_related('movie').order_by('-sale_date')
    
    if request.method == 'POST':
        form = UserEmailForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Email успешно обновлен!')
            return redirect('profile')
    else:
        form = UserEmailForm(instance=user)
    
    context = {
        'form': form,
        'purchases': purchases,
    }
    return render(request, 'profile.html', context)

def homepage(request):
    movies_list = Movie.objects.all()
    context = {
        'movies_list': movies_list,
        }
    return render(request, 'home.html', context)

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')    

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, movie_id=movie_id)
    crew_by_roles = {}
    for crew in movie.moviecrew_set.all().select_related('artist', 'role'):
        role_name = crew.role.role_name
        if role_name not in crew_by_roles:
            crew_by_roles[role_name] = []
        crew_by_roles[role_name].append(crew)
    
    context = {
        'movie': movie,
        'crew_by_roles': crew_by_roles,
        'id': movie_id,
    }
    return render(request, 'movie_detail.html', context)  

def artist_detail(request, artist_id):
    artist = get_object_or_404(Artist.objects.prefetch_related(
        'moviecrew_set__movie',
        'moviecrew_set__role'
    ), artist_id=artist_id)
    
    # Получаем фильмы с группировкой по ролям
    movies_by_role = {}
    for crew in artist.moviecrew_set.all():
        role_name = crew.role.role_name
        if role_name not in movies_by_role:
            movies_by_role[role_name] = []
        movies_by_role[role_name].append({
            'movie': crew.movie,
            'character_name': crew.character_name
        })
    
    # Статистика по ролям
    role_stats = artist.moviecrew_set.values(
        'role__role_name'
    ).annotate(
        count=Count('artist_id')
    ).order_by('-count')
    
    context = {
        'artist': artist,
        'movies_by_role': movies_by_role,
        'role_stats': role_stats,
        'age': artist.get_age(),
    }
    return render(request, 'artist_detail.html', context)   