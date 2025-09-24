from django.contrib import admin
from .models import Sale, MovieCrew, Movie, Artist, Role

#регистрация моделей в админ панели
admin.site.register(Movie) 
admin.site.register(Sale) 
admin.site.register(MovieCrew) 
admin.site.register(Artist) 
admin.site.register(Role) 