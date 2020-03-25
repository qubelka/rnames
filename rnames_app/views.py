# 2020.02.12 Kari Lintulaakso
# Most of the views use both filters and pagination
# Basic filtering is from https://django-filter.readthedocs.io/en/master/guide/usage.html
# These two are combined using a solution provided by 'Reinstate Monica'
# at https://stackoverflow.com/questions/2047622/how-to-paginate-django-with-other-get-variables/57899037#57899037

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.edit import CreateView, UpdateView, DeleteView
#from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Location, Name, Qualifier, QualifierName, Relation, Reference, StratigraphicQualifier, StructuredName
from .filters import LocationFilter, NameFilter, QualifierFilter, QualifierNameFilter, ReferenceFilter, RelationFilter, StratigraphicQualifierFilter, StructuredNameFilter
from .forms import LocationForm, NameForm, QualifierForm, QualifierNameForm, ReferenceForm, ReferenceRelationForm, RelationForm, StratigraphicQualifierForm, StructuredNameForm
from django.contrib.auth.models import User
from .filters import UserFilter
#, APINameFilter


#def name_list(request):
#    names = Name.objects.is_active().order_by('name')
#    names = Name.objects.order_by('name')
#    return render(request, 'name_list.html', {'names': names})

def help_database_structure(request):
    """
    View function for the database structure help page of site.
    """
    return render(
        request,
        'help_database_structure.html',
    )

def help_faq(request):
    """
    View function for the help page of site.
    """
    return render(
        request,
        'help_faq.html',
    )

def help_instruction(request):
    """
    View function for the instructions page of site.
    """
    return render(
        request,
        'help_instruction.html',
    )

def help_main(request):
    """
    View function for the help page of site.
    """
    return render(
        request,
        'help.html',
    )

def help_structure_of_binning_algorithm(request):
    """
    View function for the structure of the binning algorithm help page of site.
    """
    return render(
        request,
        'help_structure_of_binning_algorithm.html',
    )

def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_names=Name.objects.is_active().count()
    num_opinions=Relation.objects.is_active().count()
    num_references=Reference.objects.is_active().count()

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'num_names':num_names,'num_opinions':num_opinions,'num_references':num_references,}, # num_visits appended
    )

def parent(request):
    return render(
        request,
        'parent.html',
    )

def child(request):
    f = RelationFilter(
                      request.GET,
                      queryset=Relation.objects.is_active().select_related().order_by('name_one')
                      )

    paginator = Paginator(f.qs, 10)

    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(
        request,
        'child.html',
        {'page_obj': page_obj, 'filter': f,}
    )

class location_delete(DeleteView):
    model = Location
    success_url = reverse_lazy('location-list')

def location_detail(request, pk):
    location = get_object_or_404(Location, pk=pk, is_active=1)
    return render(request, 'location_detail.html', {'location': location})

@login_required
def location_edit(request, pk):
    location = get_object_or_404(Location, pk=pk, is_active=1)
    if request.method == "POST":
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            location = form.save(commit=False)
            location.save()
            return redirect('location-detail', pk=location.pk)
    else:
        form = LocationForm(instance=location)
    return render(request, 'location_edit.html', {'form': form})

def location_list(request):
    f = LocationFilter(request.GET, queryset=Location.objects.is_active().order_by('name'))

    paginator = Paginator(f.qs, 10)

    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(
        request,
        'location_list.html',
        {'page_obj': page_obj, 'filter': f,}
    )

@login_required
def location_new(request):
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.created_by_id = request.user.id
            location.created_on = timezone.now()
            location.save()
            return redirect('location-detail', pk=location.pk)
    else:
        form = LocationForm()
    return render(request, 'location_edit.html', {'form': form})

class name_delete(DeleteView):
    model = Name
    success_url = reverse_lazy('name-list')

def name_detail(request, pk):
    name = get_object_or_404(Name, pk=pk, is_active=1)
    return render(request, 'name_detail.html', {'name': name})

@login_required
def name_edit(request, pk):
    name = get_object_or_404(Name, pk=pk, is_active=1)
    if request.method == "POST":
        form = NameForm(request.POST, instance=name)
        if form.is_valid():
            name = form.save(commit=False)
            name.save()
            return redirect('name-detail', pk=name.pk)
    else:
        form = NameForm(instance=name)
    return render(request, 'name_edit.html', {'form': form})

def name_list(request):
    f = NameFilter(
                      request.GET,
                      queryset=Name.objects.is_active().order_by('name')
                      )

    paginator = Paginator(f.qs, 10)

    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(
        request,
        'name_list.html',
        {'page_obj': page_obj, 'filter': f,}
    )

@login_required
def name_new(request):
    if request.method == "POST":
        form = NameForm(request.POST)
        if form.is_valid():
            name = form.save(commit=False)
#            name.created_by_id = request.user.id
#            name.created_at = timezone.now()
            name.save()
            return redirect('name-detail', pk=name.pk)
    else:
        form = NameForm()
    return render(request, 'name_edit.html', {'form': form})

class qualifier_delete(DeleteView):
    model = Qualifier
    success_url = reverse_lazy('qualifier-list')

def qualifier_detail(request, pk):
    qualifier = get_object_or_404(Qualifier, pk=pk, is_active=1)
    return render(request, 'qualifier_detail.html', {'qualifier': qualifier})

def qualifier_list(request):
    f = QualifierFilter(request.GET, queryset=Qualifier.objects.is_active().select_related().order_by('stratigraphic_qualifier', 'level', 'qualifier_name',))
    paginator = Paginator(f.qs, 10)

    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(
        request,
        'qualifier_list.html',
        {'page_obj': page_obj, 'filter': f,}
    )

@login_required
def qualifier_new(request):
    if request.method == "POST":
        form = QualifierForm(request.POST)
        if form.is_valid():
            qualifier = form.save(commit=False)
            qualifier.save()
            return redirect('qualifier-detail', pk=qualifier.pk)
    else:
        form = QualifierForm()
    return render(request, 'qualifier_edit.html', {'form': form})

@login_required
def qualifier_edit(request, pk):
    qualifier = get_object_or_404(Qualifier, pk=pk, is_active=1)
    if request.method == "POST":
        form = QualifierForm(request.POST, instance=qualifier)
        if form.is_valid():
            qualifier = form.save(commit=False)
            qualifier.save()
            return redirect('qualifier-detail', pk=qualifier.pk)
    else:
        form = QualifierForm(instance=qualifier)
    return render(request, 'qualifier_edit.html', {'form': form})

class qualifiername_delete(DeleteView):
    model = QualifierName
    success_url = reverse_lazy('qualifiername-list')

def qualifiername_detail(request, pk):
    qualifiername = get_object_or_404(QualifierName, pk=pk, is_active=1)
    return render(request, 'qualifiername_detail.html', {'qualifiername': qualifiername})

@login_required
def qualifiername_edit(request, pk):
    qualifiername = get_object_or_404(QualifierName, pk=pk, is_active=1)
    if request.method == "POST":
        form = QualifierNameForm(request.POST, instance=qualifiername)
        if form.is_valid():
            qualifiername = form.save(commit=False)
            qualifiername.save()
            return redirect('qualifier-name-detail', pk=qualifiername.pk)
    else:
        form = QualifierNameForm(instance=qualifiername)
    return render(request, 'qualifiername_edit.html', {'form': form})

def qualifiername_list(request):
    f = QualifierNameFilter(
                      request.GET,
                      queryset=QualifierName.objects.is_active().order_by('name')
                      )

    paginator = Paginator(f.qs, 10)

    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(
        request,
        'qualifiername_list.html',
        {'page_obj': page_obj, 'filter': f,}
    )

@login_required
def qualifiername_new(request):
    if request.method == "POST":
        form = QualifierNameForm(request.POST)
        if form.is_valid():
            qualifiername = form.save(commit=False)
            qualifiername.save()
            return redirect('qualifier-name-detail', pk=qualifiername.pk)
    else:
        form = QualifierNameForm()
    return render(request, 'qualifiername_edit.html', {'form': form})

class reference_delete(DeleteView):
    model = Reference
    success_url = reverse_lazy('reference-list')

def reference_detail(request, pk):
    reference = get_object_or_404(Reference, pk=pk, is_active=1)
    f = RelationFilter(
                  request.GET,
                  queryset=Relation.objects.is_active().select_related().filter(reference__id=pk).order_by('name_one')
                  )

    paginator = Paginator(f.qs, 5)

    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'reference_detail.html', {'reference': reference, 'page_obj': page_obj, 'filter': f,})

@login_required
def reference_edit(request, pk):
    reference = get_object_or_404(Reference, pk=pk, is_active=1)
    if request.method == "POST":
        form = ReferenceForm(request.POST, instance=reference)
        if form.is_valid():
            reference = form.save(commit=False)
            reference.save()
            return redirect('reference-detail', pk=reference.pk)
    else:
        form = ReferenceForm(instance=reference)
    return render(request, 'reference_edit.html', {'form': form})

# If you want to access the filtered objects in your views,
# for example if you want to paginate them, you can do that.
# They are in f.qs
# view function
def reference_list_old(request):
    f = ReferenceFilter(request.GET, queryset=Reference.objects.is_active().order_by('title'))
    paginator = Paginator(f.qs, 10) # Show 10 References per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'reference_list.html', {'filter': f}, {'page_obj': page_obj})
#    return render(request, 'reference_list.html', {'filter': page_obj})
#    return render(request, 'reference_list.html', {'filter': f})

def reference_list(request):
    f = ReferenceFilter(request.GET, queryset=Reference.objects.is_active().order_by('title'))
    paginator = Paginator(f.qs, 10)

    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(
        request,
        'reference_list.html',
        {'page_obj': page_obj, 'filter': f,}
    )

@login_required
def reference_new(request):
    if request.method == "POST":
        form = ReferenceForm(request.POST)
        if form.is_valid():
            reference = form.save(commit=False)
            reference.save()
            return redirect('reference-detail', pk=reference.pk)
    else:
        form = ReferenceForm()
    return render(request, 'reference_edit.html', {'form': form})

class old_reference_relation_delete(DeleteView):
    model = Relation
    def get_object(self, queryset=None):
        obj = super(reference_relation_delete, self).get_object()
        if not obj.reference:
            raise Http404
        return obj
    success_url = reverse_lazy('reference-detail')

# https://stackoverflow.com/questions/52065046/django-deleteview-pass-argument-from-foreignkeys-model-to-get-success-url
class reference_relation_delete(DeleteView):
    model = Relation
    def get_success_url(self):
        reference = self.object.reference
        return reverse_lazy('reference-detail', kwargs={'pk': reference.pk})

@login_required
def reference_relation_new(request, reference):
    reference = get_object_or_404(Reference, pk=reference, is_active=1)
    if request.method == "POST":
        form = ReferenceRelationForm(request.POST)
        if form.is_valid():
            relation = form.save(commit=False)
            relation.reference = reference
            relation.save()
            return redirect('reference-detail', pk=relation.reference.id)
    else:
        form = ReferenceRelationForm()
    return render(request, 'relation_edit.html', {'form': form})

class relation_delete(DeleteView):
    model = Relation
    success_url = reverse_lazy('relation-list')

def relation_detail(request, pk):
    relation = get_object_or_404(Relation, pk=pk, is_active=1)
    return render(request, 'relation_detail.html', {'relation': relation})

@login_required
def relation_edit(request, pk):
    relation = get_object_or_404(Relation, pk=pk, is_active=1)
    if request.method == "POST":
        form = RelationForm(request.POST, instance=relation)
        if form.is_valid():
            relation = form.save(commit=False)
            relation.save()
            return redirect('relation-detail', pk=relation.pk)
    else:
        form = RelationForm(instance=relation)
    return render(request, 'relation_edit.html', {'form': form})

# https://docs.djangoproject.com/en/3.0/topics/pagination/
# https://django-filter.readthedocs.io/en/master/guide/usage.html
def relation_list(request):
    f = RelationFilter(
                      request.GET,
                      queryset=Relation.objects.is_active().select_related().order_by('name_one')
                      )

    paginator = Paginator(f.qs, 10)

    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(
        request,
        'relation_list.html',
        {'page_obj': page_obj, 'filter': f,}
    )

@login_required
def relation_new(request, reference_id):
    if request.method == "POST":
        form = RelationForm(request.POST)
        if form.is_valid():
            relation = form.save(commit=False)
            relation.save()
            return redirect('relation-detail', pk=relation.pk)
    else:
        form = RelationForm()
    return render(request, 'relation_edit.html', {'form': form})

def rnames_detail(request):
    return render(request, 'rnames_detail.html', )

@login_required
def run_binning(request):
    """
    View function for the run binning operation.
    """
    # Generate counts of some of the main objects
    num_opinions=Relation.objects.is_active().count()

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'run_binning.html',
        context={'num_opinions':num_opinions,},
    )

class stratigraphic_qualifier_delete(DeleteView):
    model = StratigraphicQualifier
    success_url = reverse_lazy('stratigraphic-qualifier-list')

def stratigraphic_qualifier_detail(request, pk):
    stratigraphicqualifier = get_object_or_404(StratigraphicQualifier, pk=pk, is_active=1)
    return render(request, 'stratigraphic_qualifier_detail.html', {'stratigraphicqualifier': stratigraphicqualifier})

@login_required
def stratigraphic_qualifier_edit(request, pk):
    stratigraphicqualifier = get_object_or_404(StratigraphicQualifier, pk=pk, is_active=1)
    if request.method == "POST":
        form = StratigraphicQualifierForm(request.POST, instance=stratigraphicqualifier)
        if form.is_valid():
            stratigraphicqualifier = form.save(commit=False)
            stratigraphicqualifier.save()
            return redirect('stratigraphic-qualifier-detail', pk=stratigraphicqualifier.pk)
    else:
        form = StratigraphicQualifierForm(instance=stratigraphicqualifier)
    return render(request, 'stratigraphic_qualifier_edit.html', {'form': form})

def stratigraphic_qualifier_list(request):
    f = StratigraphicQualifierFilter(
                      request.GET,
                      queryset=StratigraphicQualifier.objects.is_active().order_by('name')
                      )

    paginator = Paginator(f.qs, 10)

    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(
        request,
        'stratigraphic_qualifier_list.html',
        {'page_obj': page_obj, 'filter': f,}
    )

@login_required
def stratigraphic_qualifier_new(request):
    if request.method == "POST":
        form = StratigraphicQualifierForm(request.POST)
        if form.is_valid():
            stratigraphicqualifier = form.save(commit=False)
            stratigraphicqualifier.save()
            return redirect('stratigraphic-qualifier-detail', pk=stratigraphicqualifier.pk)
    else:
        form = StratigraphicQualifierForm()
    return render(request, 'stratigraphic_qualifier_edit.html', {'form': form})

class structuredname_delete(DeleteView):
    model = StructuredName
    success_url = reverse_lazy('structuredname-list')

def structuredname_detail(request, pk):
    structuredname = get_object_or_404(StructuredName, pk=pk, is_active=1)
    return render(request, 'structuredname_detail.html', {'structuredname': structuredname})

def structuredname_list(request):
    f = StructuredNameFilter(request.GET, queryset=StructuredName.objects.is_active().select_related().order_by('name', 'qualifier', 'location'))
    paginator = Paginator(f.qs, 10)

    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(
        request,
        'structuredname_list.html',
        {'page_obj': page_obj, 'filter': f,}
    )

@login_required
def structuredname_new(request):
    if request.method == "POST":
        form = StructuredNameForm(request.POST)
        if form.is_valid():
            structuredname = form.save(commit=False)
            structuredname.save()
            return redirect('structuredname-detail', pk=structuredname.pk)
    else:
        form = StructuredNameForm()
    return render(request, 'structuredname_edit.html', {'form': form})

@login_required
def structuredname_edit(request, pk):
    structuredname = get_object_or_404(StructuredName, pk=pk, is_active=1)
    if request.method == "POST":
        form = StructuredNameForm(request.POST, instance=structuredname)
        if form.is_valid():
            structuredname = form.save(commit=False)
            structuredname.save()
            return redirect('structuredname-detail', pk=structuredname.pk)
    else:
        form = StructuredNameForm(instance=structuredname)
    return render(request, 'structuredname_edit.html', {'form': form})

def user_search(request):
    user_list = User.objects.all()
    user_filter = UserFilter(request.GET, queryset=user_list)
    return render(request, 'user_list.html', {'filter': user_filter})
