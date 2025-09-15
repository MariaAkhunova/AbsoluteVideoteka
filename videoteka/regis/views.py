# views.py
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Sale, MovieCrew, Movie, Artist, Role

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
    return render(request, 'artist_detail.html')   