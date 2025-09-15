# views.py
from django.shortcuts import render, redirect,  get_object_or_404
from django.db.models import Count
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Sale, MovieCrew, Movie, Artist, Role
from datetime import date

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