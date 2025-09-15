from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("home/", views.homepage, name="home"),
    path('logout/', views.logout_view, name='logout'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
]