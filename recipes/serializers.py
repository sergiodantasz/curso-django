from rest_framework import serializers

from authors.models import User
from recipes.models import Category
from tag.models import Tag


class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    slug = serializers.SlugField()


class RecipeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=65)
    description = serializers.CharField(max_length=165)
    public = serializers.BooleanField(source='is_published')
    preparation = serializers.SerializerMethodField(method_name='any_method_name')
    category = serializers.StringRelatedField()
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    author = serializers.StringRelatedField()
    author_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    tag_objects = TagSerializer(source='tags', many=True)
    tag_links = serializers.HyperlinkedRelatedField(
        source='tags',
        many=True,
        queryset=Tag.objects.all(),
        view_name='recipes:api_v2_tag',
    )

    def any_method_name(self, obj):
        return f'{obj.preparation_time} {obj.preparation_time_unit}'
