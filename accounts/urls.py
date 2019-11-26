from django.urls import path
from . import views

app_name = 'accounts'

# urlpatterns 비어있더라도 만들어야 오류 방지

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
    path('password/', views.password, name='password'), 
]