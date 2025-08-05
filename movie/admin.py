
from django.contrib import admin
from movie.models import Genre, Content, Profile, WatchedHistory

admin.site.register([Genre, Content, Profile, WatchedHistory])
