from django.urls import path
from movie import views

urlpatterns = [
    path('', views.genre_list_or_create),
    path('<int:pk>/', views.genre_retrive_update_or_delete),
    path('contents/', views.content_list_or_create),
    path('contents/<int:pk>/', views.content_retrive_update_or_delete),
    path('users/', views.user_list_or_create),
    path('users/<int:pk>/', views.user_retrive_update_or_delete),
    path('nt-users/', views.user_nested_list_or_create),
    path('nt-users/<int:pk>/', views.user_nested_retrieve_update_or_delete)

]