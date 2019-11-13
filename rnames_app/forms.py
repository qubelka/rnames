from django import forms

from .models import Location, Name, Qualifier, Reference, Relation, StructuredName

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

class ReferenceForm(forms.ModelForm):
#    title = forms.CharField(widget=forms.Textarea)
    link = forms.CharField(widget=forms.Textarea(attrs={'cols': 100, 'rows': 1}))
    class Meta:
        model = Reference
        fields = ('first_author','year','title','link',)

class RelationForm(forms.ModelForm):
#    title = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Relation
        fields = ('name_one','name_two','belongs_to','reference',)

class StructuredNameForm(forms.ModelForm):

    class Meta:
        model = StructuredName
        fields = ('qualifier','name','location',)
