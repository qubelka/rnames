from django import forms
from django_select2.forms import (
    ModelSelect2Widget,
)
from .models import Location, Name, Qualifier, QualifierName, Reference, Relation, StratigraphicQualifier, StructuredName

class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = ('name',)

class NameForm(forms.ModelForm):

    class Meta:
        model = Name
        fields = ('name',)

class QualifierForm(forms.ModelForm):

    class Meta:
        model = Qualifier
        fields = ('qualifier_name', 'stratigraphic_qualifier', 'level',)

class QualifierNameForm(forms.ModelForm):

    class Meta:
        model = QualifierName
        fields = ('name',)

class ReferenceForm(forms.ModelForm):
#    title = forms.CharField(widget=forms.Textarea)
    link = forms.CharField(widget=forms.Textarea(attrs={'cols': 100, 'rows': 1}))
    class Meta:
        model = Reference
        fields = ('first_author','year','title','doi','link',)

class ReferenceWidget(ModelSelect2Widget):
    search_fields = ['title__icontains', 'first_author__icontains',]

class RelationWidget(ModelSelect2Widget):
    search_fields = ['name__name__icontains', 'location__name__icontains', 'qualifier__qualifier_name__name__icontains', 'qualifier__stratigraphic_qualifier__name__icontains',]

class RelationForm(forms.ModelForm):
    class Meta:
        model = Relation
        fields = ('name_one', 'name_two', 'belongs_to', 'reference',)
        widgets = {'name_one': RelationWidget, 'name_two': RelationWidget, 'reference': ReferenceWidget,}

# For StructuredNameForm:
class LocationWidget(ModelSelect2Widget):
    search_fields = ['name__icontains',]

# For StructuredNameForm:
class NameWidget(ModelSelect2Widget):
    search_fields = ['name__icontains',]

# For StructuredNameForm:
class QualifierWidget(ModelSelect2Widget):
    search_fields = ['qualifier_name__name__icontains', 'stratigraphic_qualifier__name__icontains',]

class StructuredNameForm(forms.ModelForm):
    class Meta:
        model = StructuredName
        fields = ('qualifier','name','location',)
        widgets = {'location': LocationWidget, 'name': NameWidget, 'qualifier': QualifierWidget, }

class StratigraphicQualifierForm(forms.ModelForm):

    class Meta:
        model = StratigraphicQualifier
        fields = ('name',)
