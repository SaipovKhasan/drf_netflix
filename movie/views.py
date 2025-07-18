from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from movie.models import Genre
from movie.serializers import GenreSerializer


@api_view(['GET'])
def get_genres(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)


def get_contents(request):
    return None