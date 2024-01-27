from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError

from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_non_negative_number


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._form_errors = defaultdict(list)
        self._form_errors
        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = (
            'title',
            'description',
            'preparation_time',
            'preparation_time_unit',
            'preparation_steps',
            'servings',
            'servings_unit',
            'cover',
        )
        widgets = {
            'cover': forms.FileInput(attrs={'class': 'span-2'}),
            'servings_unit': forms.Select(
                choices=(
                    ('Porcões', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            ),
        }

    def clean(self):
        clean_ = super().clean()
        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        if title == description:
            self._form_errors['description'].append(
                'The title and description must be different.'
            )
        if self._form_errors:
            raise ValidationError(self._form_errors)
        return clean_

    def clean_title(self):
        field_name = 'title'
        field_value = self.cleaned_data.get(field_name)
        if len(field_value) < 5:
            self._form_errors[field_name].append(
                'The title must have at least 5 characters.'
            )
        return field_value

    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.cleaned_data.get(field_name)
        if not is_non_negative_number(field_value):
            self._form_errors[field_name].append(
                'The preparation time must be a non-negative number.'
            )
        return field_value

    def clean_servings(self):
        field_name = 'servings'
        field_value = self.cleaned_data.get(field_name)
        if not is_non_negative_number(field_value):
            self._form_errors[field_name].append(
                'The servings must be a non-negative number.'
            )
        return field_value
