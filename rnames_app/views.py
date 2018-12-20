from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Name
from .forms import NameForm

def name_list(request):
    names = Name.objects.order_by('name')
    return render(request, 'rnames_app/name_list.html', {'names': names})

def name_detail(request, pk):
    name = get_object_or_404(Name, pk=pk)
    return render(request, 'rnames_app/name_detail.html', {'name': name})

def name_new(request):
    if request.method == "POST":
        form = NameForm(request.POST)
        if form.is_valid():
            name = form.save(commit=False)
            name.created_by_id = request.user.id
            name.created_at = timezone.now()
            name.save()
            return redirect('name_detail', pk=name.pk)
    else:
        form = NameForm()
    return render(request, 'rnames_app/name_edit.html', {'form': form})

def name_edit(request, pk):
    name = get_object_or_404(Name, pk=pk)
    if request.method == "POST":
        form = NameForm(request.POST, instance=name)
        if form.is_valid():
            name = form.save(commit=False)
            name.created_by_id = request.user.id
            name.created_at = timezone.now()
            name.save()
            return redirect('name_detail', pk=name.pk)
    else:
        form = NameForm(instance=name)
    return render(request, 'rnames_app/name_edit.html', {'form': form})

def qualifier_detail(request, pk):
    qualifier = get_object_or_404(Qualifier, pk=pk)
    return render(request, 'rnames_app/qualifier_detail.html', {'qualifier': qualifier})
