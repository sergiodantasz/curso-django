from django.urls import path

from recipes.views import about, contact, home

urlpatterns = [
    path('', home),
    path('about/', about),
    path('contact/', contact),
]
