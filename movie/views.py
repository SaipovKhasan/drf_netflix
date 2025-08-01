from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from movie.models import Genre, Content, User
from movie.serializers import GenreSerializer, ContentSerializer, UserProfileSerializer, UserSerializer
from django.db.models import Q


# CRUD
@api_view(['GET', 'POST'])
def genre_list_or_create(request, format=None):
    if request.method == 'GET':
        genres = Genre.objects.all()
        search = request.query_params.get('search', None)
        if search:
            genres = genres.filter(name__icontains=search)
        serializer = GenreSerializer(genres, many=True)
        content = Content.objects.filter(genres__in=genres).count()
        return Response({
            "total_genres": genres.count(),
            "total_films": content,
            "genres": serializer.data},
            status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def genre_retrive_update_or_delete(request, pk, format=None):
    try:
        genre = Genre.objects.get(id=pk)
    except Genre.DoesNotExist:
        return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = GenreSerializer(genre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        genre.delete()
        return Response({"message": "Object is deleted!"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def content_list_or_create(request, format=None):
    if request.method == 'GET':
        genre = request.query_params.get('genre')
        director = request.query_params.get('director')
        title = request.query_params.get('title')
        desc = request.query_params.get('desc')

        filters = Q()
        if genre:
            filters &= Q(genres__name__icontains=genre)

        if director:
            filters &= Q(director__icontains=director)

        if title:
            filters &= Q(title__icontains=title)

        if desc:
            filters &= Q(description__icontains=desc)

        contents = Content.objects.filter(filters).distinct()

        serializer = ContentSerializer(contents, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def content_retrive_update_or_delete(request, pk, format=None):
    try:
        content = Content.objects.get(id=pk)
    except Content.DoesNotExist:
        return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ContentSerializer(content)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = ContentSerializer(content, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = ContentSerializer(content, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        content.delete()
        return Response({"message": "Object is deleted!"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def user_list_or_create(request, format=None):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserProfileSerializer(users, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = UserProfileSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        print(serializer.initial_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PATCH', 'DELETE'])
def user_retrive_update_or_delete(request, pk, format=None):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({"message": "User object not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserProfileSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        serializer = UserProfileSerializer(user, data=request.data, context={'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        user.delete()
        return Response({"message": "Object is deleted!"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def user_nested_list_or_create(request, format=None):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PATCH', "DELETE"])
def user_nested_retrieve_update_or_delete(request, pk, format=None):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({"message": "User object not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user, context={"request": request, "user": user})
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data, context={"request": request, "user": user}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == "DELETE":
        user.delete()
        return Response({"message": "Object is deleted!"}, status=status.HTTP_204_NO_CONTENT)