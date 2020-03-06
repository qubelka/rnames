# 2020.02.12 Kari Lintulaakso
# Most of the views use both filters and pagination
# Basic filtering is from https://django-filter.readthedocs.io/en/master/guide/usage.html
# These two are combined using a solution provided by 'Reinstate Monica'
# at https://stackoverflow.com/questions/2047622/how-to-paginate-django-with-other-get-variables/57899037#57899037

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
from .forms import LocationForm, NameForm, QualifierForm, QualifierNameForm, ReferenceForm, RelationForm, StratigraphicQualifierForm, StructuredNameForm
from django.contrib.auth.models import User
from .filters import UserFilter
#, APINameFilter


#def name_list(request):
#    names = Name.objects.is_active().order_by('name')
#    names = Name.objects.order_by('name')
#    return render(request, 'name_list.html', {'names': names})

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
        'base_generic.html',
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
                      queryset=Relation.objects.is_active().order_by('name_one')
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
    location = get_object_or_404(Location, pk=pk)
    return render(request, 'location_detail.html', {'location': location})

def location_edit(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == "POST":
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            location = form.save(commit=False)
            location.modified_by_id = request.user.id
            location.modified_on = timezone.now()
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
    name = get_object_or_404(Name, pk=pk)
    return render(request, 'name_detail.html', {'name': name})

def name_edit(request, pk):
    name = get_object_or_404(Name, pk=pk)
    if request.method == "POST":
        form = NameForm(request.POST, instance=name)
        if form.is_valid():
            name = form.save(commit=False)
#            name.created_by_id = request.user.id
#            name.created_at = timezone.now()
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
    qualifier = get_object_or_404(Qualifier, pk=pk)
    return render(request, 'qualifier_detail.html', {'qualifier': qualifier})

def qualifier_list(request):
    f = QualifierFilter(request.GET, queryset=Qualifier.objects.is_active().order_by('stratigraphic_qualifier', 'level', 'qualifier_name',))

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

def qualifier_edit(request, pk):
    qualifier = get_object_or_404(Qualifier, pk=pk)
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
    qualifiername = get_object_or_404(QualifierName, pk=pk)
    return render(request, 'qualifiername_detail.html', {'qualifiername': qualifiername})

def qualifiername_edit(request, pk):
    qualifiername = get_object_or_404(QualifierName, pk=pk)
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
    reference = get_object_or_404(Reference, pk=pk)
    return render(request, 'reference_detail.html', {'reference': reference})

def reference_edit(request, pk):
    reference = get_object_or_404(Reference, pk=pk)
    if request.method == "POST":
        form = ReferenceForm(request.POST, instance=reference)
        if form.is_valid():
            reference = form.save(commit=False)
#            name.created_by_id = request.user.id
#            name.created_at = timezone.now()
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
    # BTW you do not need .all() after a .filter()
    # local_url.objects.filter(global_url__id=1) will do
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

class relation_delete(DeleteView):
    model = Relation
    success_url = reverse_lazy('relation-list')

def relation_detail(request, pk):
    relation = get_object_or_404(Relation, pk=pk)
    return render(request, 'relation_detail.html', {'relation': relation})

def relation_edit(request, pk):
    relation = get_object_or_404(Relation, pk=pk)
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
                      queryset=Relation.objects.is_active().order_by('name_one')
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

def relation_new(request):
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

class stratigraphic_qualifier_delete(DeleteView):
    model = StratigraphicQualifier
    success_url = reverse_lazy('stratigraphic-qualifier-list')

def stratigraphic_qualifier_detail(request, pk):
    stratigraphicqualifier = get_object_or_404(StratigraphicQualifier, pk=pk)
    return render(request, 'stratigraphic_qualifier_detail.html', {'stratigraphicqualifier': stratigraphicqualifier})

def stratigraphic_qualifier_edit(request, pk):
    stratigraphicqualifier = get_object_or_404(StratigraphicQualifier, pk=pk)
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
    structuredname = get_object_or_404(StructuredName, pk=pk)
    return render(request, 'structuredname_detail.html', {'structuredname': structuredname})

def structuredname_list(request):
    f = StructuredNameFilter(request.GET, queryset=StructuredName.objects.is_active().order_by('name', 'qualifier', 'location'))

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

def structuredname_edit(request, pk):
    structuredname = get_object_or_404(StructuredName, pk=pk)
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
