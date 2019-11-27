from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/like/', views.like, name='like'),
    path('<int:movie_pk>/rating/', views.rating, name='rating'),
    path('<int:rating_pk>/update/', views.update_rating, name ='update_rating'),
    path('<int:rating_pk>/delete/', views.delete_rating, name='delete_rating'),
    path('getmovies/', views.getmovies, name='getmovies'),
    path('get_like_genres/', views.get_like_genres, name='get_like_genres'),
    

]
