from rest_framework import serializers

from authors.models import User
from authors.validators import AuthorRecipeValidator
from recipes.models import Category, Recipe
from tag.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

    # id = serializers.IntegerField()
    # name = serializers.CharField(max_length=255)
    # slug = serializers.SlugField()


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'description',
            'category',
            'public',
            'preparation',
            'author',
            'tags',
            'tag_objects',
            'tag_links',
            'preparation_time',
            'preparation_time_unit',
            'servings',
            'servings_unit',
            'preparation_steps',
            'cover',
        ]

    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=65)
    # description = serializers.CharField(max_length=165)
    public = serializers.BooleanField(source='is_published', read_only=True)
    preparation = serializers.SerializerMethodField(
        method_name='any_method_name', read_only=True
    )
    category = serializers.StringRelatedField(read_only=True)
    # category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    author = serializers.StringRelatedField()
    # author_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    tag_objects = TagSerializer(source='tags', many=True)
    tag_links = serializers.HyperlinkedRelatedField(
        source='tags',
        many=True,
        queryset=Tag.objects.all(),
        view_name='recipes:api_v2_tag',
    )

    def any_method_name(self, obj):
        return f'{obj.preparation_time} {obj.preparation_time_unit}'

    def validate(self, attrs):
        if self.instance is not None and attrs.get('servings') is None:
            attrs['servings'] = self.instance.servings

        if self.instance is not None and attrs.get('preparation_time') is None:
            attrs['preparation_time'] = self.instance.preparation_time
        super_validate = super().validate(attrs)
        AuthorRecipeValidator(
            data=attrs,
            ErrorClass=serializers.ValidationError,
        )
        return super_validate

    def save(self, **kwargs):
        return super().save(**kwargs)

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
