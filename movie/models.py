
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models

User = get_user_model()


class TimeStempModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Genre(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return f"{self.name}"


class Content(TimeStempModel):
    genre = models.ManyToManyField(Genre, related_name='contents')
    director = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True,
                                   validators=[
                                       MinLengthValidator(20),
                                       MaxLengthValidator(1000)
                                   ],
                                   help_text='Belgilar soni 20-1000 oraligidi bo`lishi shart.')
    thumbnail_url = models.URLField()
    trailer = models.URLField(null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    duration = models.PositiveSmallIntegerField(help_text='Second')
    release_date = models.DateField()

    def __str__(self):
        return f'{self.director} {self.title}'

    class Meta:
        unique_together = ('title', 'director')
        ordering = ['-release_date']
