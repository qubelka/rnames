from django.shortcuts import render

def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    #num_names=Name.objects.is_active().count()
    #num_opinions=Relation.objects.is_active().count()
    #num_references=Reference.objects.is_active().count()

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'now/base_generic.html',
#        context={'num_names':num_names,'num_opinions':num_opinions,'num_references':num_references,}, # num_visits appended
    )
