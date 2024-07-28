from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('friends', views.friends)
]