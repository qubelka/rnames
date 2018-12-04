from django.shortcuts import render

def name_list(request):
    return render(request, 'rnames_app/name_list.html', {})
