from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User

class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return f"{self.role_name}"

    class Meta:
        db_table = 'roles'

class Artist(models.Model):
    artist_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True, blank=True)
    biography = models.CharField(max_length=500, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'artists'

class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    release_year = models.IntegerField()
    genre = models.CharField(max_length=100)
    duration = models.IntegerField()
    price = models.IntegerField()
    poster = models.ImageField(upload_to='poster/', null=True, blank=True)
    description = models.CharField(max_length=255)
    trailer_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.title} - {self.price} руб."

    class Meta:
        db_table = 'movies'

class MovieCrew(models.Model):
    crew_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='movie_id')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, db_column='artist_id')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_column='role_id')
    character_name = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.movie} - {self.artist} - {self.character_name}"

    class Meta:
        db_table = 'movie_crew'

class Sale(models.Model):
    sale_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, db_column='movie_id')
    unit_price = models.IntegerField()
    sale_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} - {self.movie}"

    class Meta:
        db_table = 'sales'
