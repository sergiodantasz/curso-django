from django.urls import path

from recipes.views import about, home

urlpatterns = [
    path('', home),
    path('about/', about),
]
