import django_filters
from .models import Name
from django.contrib.auth.models import User
from django_filters import rest_framework as filters


class NameFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Name
        fields = ['name', 'created_by__first_name', ]

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', ]


class APINameFilter(filters.FilterSet):
#    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Name
        fields = ['name', 'created_by__first_name', ]
