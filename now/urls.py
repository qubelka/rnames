from django.conf.urls import url
from django.urls import path, re_path
from . import views
#from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
#    path('rnames/', views.name_list, name='name_list'),
#    path('rnames/name/<int:pk>/', views.name_detail, name='name_detail'),
#    path('rnames/name/new', views.name_new, name='name_new'),
#    path('rnames/name/<int:pk>/edit/', views.name_edit, name='name_edit'),
#    path('rnames/qualifier/<int:pk>/', views.qualifier_detail, name='qualifier-detail'),
#    path('mb/names/', views.MasterReferenceListView.as_view(), name='names'),
    path('now/', views.index, name='index'),
    path('now/acknowledgements/', views.acknowledgements, name='acknowledgements'),
    path('now/board/', views.board, name='board'),
    path('now/contact/', views.contact, name='contact'),
    path('now/conventions/', views.conventions, name='conventions'),
    path('now/database/', views.database, name='database'),
    path('now/ecometrics/', views.ecometrics, name='ecometrics'),
    path('now/export_maps/', views.export_maps, name='export_maps'),
    path('now/faq/', views.faq, name='faq'),
    path('now/field_archive/', views.field_archive, name='field_archive'),
    path('now/links/', views.links, name='links'),
    path('now/publications/', views.publications, name='publications'),
]

#urlpatterns = format_suffix_patterns(urlpatterns)
