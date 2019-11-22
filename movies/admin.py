from django.contrib import admin
from .models import Genre,Actor,Director,Movie,Rating,User
# Register your models here.

admin.site.register(Genre)
admin.site.register(User)
admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Movie)
admin.site.register(Rating)