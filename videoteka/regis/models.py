from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50, unique=True)
    
    class Meta:
        db_table = 'roles'

class Artist(models.Model):
    artist_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True, blank=True)
    biography = models.CharField(max_length=500, blank=True)
    
    class Meta:
        db_table = 'artists'

class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    release_year = models.IntegerField()
    genre = models.CharField(max_length=100)
    duration = models.IntegerField()
    price = models.IntegerField()
    poster = models.ImageField(upload_to='poster/', null=True)
    
    class Meta:
        db_table = 'movies'

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'

class MovieCrew(models.Model):
    crew_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='movie_id')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, db_column='artist_id')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_column='role_id')
    character_name = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        db_table = 'movie_crew'

class Sale(models.Model):
    sale_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='movie_id')
    unit_price = models.IntegerField()
    sale_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'sales'
