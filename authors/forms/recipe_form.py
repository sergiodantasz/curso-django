from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError

from authors.validators import AuthorRecipeValidator
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
        AuthorRecipeValidator(self.cleaned_data, ErrorClass=ValidationError)
        return clean_
