from random import SystemRandom
from string import ascii_letters, digits

from django.utils.text import slugify


def generate_random_characters(k: int = 5):
    return ''.join(SystemRandom().choices(ascii_letters + digits, k=k))


def generate_slug(string: str, k: int = 5):
    if k == 0:
        return slugify(string)
    return slugify(string) + '-' + generate_random_characters(k)


def generate_dynamic_slug(instance, field):
    model = instance.__class__
    field_value = getattr(instance, field)
    slug = generate_slug(field_value, 0)
    k = 1
    while True:
        data = model.objects.filter(slug=slug)
        if len(data) == 0:
            break
        slug = generate_slug(field_value, k)
        k += 1
    return slug
