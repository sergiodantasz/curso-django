from django.urls import path
from rest_framework.routers import SimpleRouter

from authors import views

app_name = 'authors'

author_api_router = SimpleRouter()
author_api_router.register('api', views.AuthorViewSet, basename='author-api')

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/create/', views.register_create, name='register_create'),
    path('login/', views.login, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout, name='logout'),
    path(
        'dashboard/recipe/new/',
        views.DashboardRecipe.as_view(),
        name='dashboard_recipe_new',
    ),
    path(
        'dashboard/recipe/delete/',
        views.DashboardRecipeDelete.as_view(),
        name='dashboard_recipe_delete',
    ),
    path(
        'dashboard/recipe/<int:id>/edit/',
        views.DashboardRecipe.as_view(),
        name='dashboard_recipe_edit',
    ),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/<int:id>/', views.ProfileView.as_view(), name='profile'),
]

urlpatterns += author_api_router.urls
