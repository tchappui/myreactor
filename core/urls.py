from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # post views
    path('', views.index, name='index'),
    path('play/data/', views.play_data, name="play_data"),
    path('play/<int:playerid>/', views.play, name='play'),
    path('play/data/score/', views.score, name="score"),
    path('info/<int:playerid>/', views.info, name='info'),
    path('register/', views.register, name='register'),
]