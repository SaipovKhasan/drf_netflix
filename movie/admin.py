from django.contrib import admin
from movie.models import Genre, Content, Profile

admin.site.register([Genre, Content, Profile])