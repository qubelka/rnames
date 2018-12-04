from django.shortcuts import render
from .models import Name

def name_list(request):
    names = Name.objects.order_by('name')
    return render(request, 'rnames_app/name_list.html', {'names': names})
