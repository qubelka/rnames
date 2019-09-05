from django.shortcuts import render
from django.views import generic
from .models import MasterEntity, MasterReference

class MasterReferenceListView(generic.ListView):
    model = MasterReference
    template_name ='mb/master_species.html'

    def get_queryset(self):
        return MasterReference.objects.order_by('-citation')

def home(request):
    taxa = MasterEntity.objects.all()
    return render(request, 'mb/master_species.html', {'taxa': taxa})
