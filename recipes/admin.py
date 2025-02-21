from django.contrib import admin

from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'created_at',
        'is_published',
    )
    list_display_links = ('title',)
    search_fields = (
        'id',
        'title',
        'description',
        'slug',
        'preparation_steps',
    )
    list_filter = (
        'category',
        'author',
        'is_published',
        'preparation_steps_is_html',
    )
    list_per_page = 30
    list_editable = ('is_published',)
    ordering = ('-id',)
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('tags',)
