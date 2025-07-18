from django.contrib import admin
from movie.models import Genre, Content

admin.site.register([Genre, Content])