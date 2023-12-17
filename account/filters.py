# filters.py
import django_filters
from .models import Profile

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = Profile
        fields = ['gender', 'relationship_goals', 'height', 'weight', 'smoking', 'alcohol', 'physique',
                  'tatu', 'piercing', 'scars', 'interests', 'hair_color', 'eye_color']
