import django_filters
from .models import Location, Name, Qualifier, Reference, Relation
from django.contrib.auth.models import User
from django_filters import rest_framework as filters


class LocationFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Location
        fields = ['name', ]

class NameFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Name
        fields = ['name', ]

class QualifierFilter(django_filters.FilterSet):
    qualifier_name__name = django_filters.CharFilter(lookup_expr='icontains')
    stratigraphic_qualifier__name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Name
        fields = ['qualifier_name__name','stratigraphic_qualifier__name', ]

class RelationFilter(django_filters.FilterSet):

    class Meta:
        model = Relation
        fields = ['name_one', 'name_two', ]

class ReferenceFilter(django_filters.FilterSet):

    class Meta:
        model = Reference
        fields = ['first_author', 'year', 'title', ]

class StructuredNameFilter(django_filters.FilterSet):
    qualifier__qualifier_name__name = django_filters.CharFilter(lookup_expr='icontains')
    qualifier__stratigraphic_qualifier__name = django_filters.CharFilter(lookup_expr='icontains')
    name__name = django_filters.CharFilter(lookup_expr='icontains')
    location__name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Name
        fields = ['name__name','qualifier__qualifier_name__name','qualifier__stratigraphic_qualifier__name','location__name', ]

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', ]


class APINameFilter(filters.FilterSet):
#    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Name
        fields = ['name', 'created_by__first_name', ]
