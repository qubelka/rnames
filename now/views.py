from django.shortcuts import render

def acknowledgements(request):
    """
    View function for acknowledgements page of site.
    """
    return render(
        request,
        'now/acknowledgements.html',
    )

def board(request):
    """
    View function for board page of site.
    """
    return render(
        request,
        'now/board.html',
    )

def contact(request):
    """
    View function for contact page of site.
    """
    return render(
        request,
        'now/contact.html',
    )

def conventions(request):
    """
    View function for conventions page of site.
    """
    return render(
        request,
        'now/conventions.html',
    )

def database(request):
    """
    View function for database page of site.
    """
    return render(
        request,
        'now/database.html',
    )

def ecometrics(request):
    """
    View function for ecometrics page of site.
    """
    return render(
        request,
        'now/ecometrics.html',
    )

def export_maps(request):
    """
    View function for export_maps page of site.
    """
    return render(
        request,
        'now/export_maps.html',
    )

def faq(request):
    """
    View function for FAQ page of site.
    """
    return render(
        request,
        'now/faq.html',
    )

def field_archive(request):
    """
    View function for field_archive page of site.
    """
    return render(
        request,
        'now/field_archive.html',
    )

def index(request):
    """
    View function for home page of site.
    """

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'now/index.html',
    )

def links(request):
    """
    View function for links page of site.
    """
    return render(
        request,
        'now/links.html',
    )

def publications(request):
    """
    View function for publications page of site.
    """
    return render(
        request,
        'now/publications.html',
    )
