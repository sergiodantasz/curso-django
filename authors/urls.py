from django.urls import path

from authors import views

app_name = 'authors'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/create/', views.register_create, name='register_create'),
    path('login/', views.login, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/recipe/new/', views.dashboard_recipe_new, name='dashboard_recipe_new'),
    path('dashboard/recipe/delete/', views.dashboard_recipe_delete, name='dashboard_recipe_delete'),
    path('dashboard/recipe/<int:id>/edit/', views.dashboard_recipe_edit, name='dashboard_recipe_edit'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
