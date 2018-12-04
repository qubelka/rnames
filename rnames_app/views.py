from django.shortcuts import render, get_object_or_404
from .models import Name

def name_list(request):
    names = Name.objects.order_by('name')
    return render(request, 'rnames_app/name_list.html', {'names': names})

def name_detail(request, pk):
    name = get_object_or_404(Name, pk=pk)
    return render(request, 'rnames_app/name_detail.html', {'name': name})
