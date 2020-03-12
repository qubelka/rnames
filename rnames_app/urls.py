from django.conf import settings
from django.conf.urls import url
from django.urls import path, re_path, include
from . import views
import debug_toolbar
#from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('rnames/parent', views.parent, name='parent'),
    path('rnames/child', views.child, name='child'),
    path('rnames/', views.name_list, name='name-list'),
    path('rnames/locations', views.location_list, name='location-list'),
    path('rnames/location/<int:pk>/', views.location_detail, name='location-detail'),
    path('rnames/location/<int:pk>/delete/', views.location_delete.as_view(), name='location-delete'),
    path('rnames/location/<int:pk>/edit/', views.location_edit, name='location-edit'),
    path('rnames/location/new', views.location_new, name='location-new'),
    path('rnames/name/new', views.name_new, name='name-new'),
    path('rnames/name/<int:pk>/', views.name_detail, name='name-detail'),
    path('rnames/name/<int:pk>/delete/', views.name_delete.as_view(), name='name-delete'),
    path('rnames/name/<int:pk>/edit/', views.name_edit, name='name-edit'),
    path('rnames/qualifiers', views.qualifier_list, name='qualifier-list'),
    path('rnames/qualifier/new', views.qualifier_new, name='qualifier-new'),
    path('rnames/qualifier/<int:pk>/', views.qualifier_detail, name='qualifier-detail'),
    path('rnames/qualifier/<int:pk>/delete/', views.qualifier_delete.as_view(), name='qualifier-delete'),
    path('rnames/qualifier/<int:pk>/edit/', views.qualifier_edit, name='qualifier-edit'),
    path('rnames/qualifier_names', views.qualifiername_list, name='qualifiername-list'),
    path('rnames/qualifier_name/new', views.qualifiername_new, name='qualifiername-new'),
    path('rnames/qualifier_name/<int:pk>/', views.qualifiername_detail, name='qualifier-name-detail'),
    path('rnames/qualifier_name/<int:pk>/delete/', views.qualifiername_delete.as_view(), name='qualifiername-delete'),
    path('rnames/qualifier_name/<int:pk>/edit/', views.qualifiername_edit, name='qualifiername-edit'),
    path('rnames/references', views.reference_list, name='reference-list'),
    path('rnames/reference/new', views.reference_new, name='reference-new'),
    path('rnames/reference/<int:pk>/', views.reference_detail, name='reference-detail'),
    path('rnames/reference/<int:pk>/delete/', views.reference_delete.as_view(), name='reference-delete'),
    path('rnames/reference/<int:pk>/edit/', views.reference_edit, name='reference-edit'),
    path('rnames/refrelation/new/<int:reference>/', views.reference_relation_new, name='reference-relation-new'),
    path('rnames/refrelation/<int:pk>/delete/', views.reference_relation_delete.as_view(), name='reference-relation-delete'),
    path('rnames/relations', views.relation_list, name='relation-list'),
    path('rnames/relation/new', views.relation_new, name='relation-new'),
    path('rnames/relation/<int:pk>/', views.relation_detail, name='relation-detail'),
    path('rnames/relation/<int:pk>/edit/', views.relation_edit, name='relation-edit'),
    path('rnames/relation/<int:pk>/delete/', views.relation_delete.as_view(), name='relation-delete'),
    path('rnames/rnames_detail', views.rnames_detail, name='rnames-detail'),
    path('rnames/stratigraphic_qualifiers', views.stratigraphic_qualifier_list, name='stratigraphic-qualifier-list'),
    path('rnames/stratigraphic_qualifier/new', views.stratigraphic_qualifier_new, name='stratigraphic-qualifier-new'),
    path('rnames/stratigraphic_qualifier/<int:pk>/', views.stratigraphic_qualifier_detail, name='stratigraphic-qualifier-detail'),
    path('rnames/stratigraphic_qualifier/<int:pk>/delete/', views.stratigraphic_qualifier_delete.as_view(), name='stratigraphic-qualifier-delete'),
    path('rnames/stratigraphic_qualifier/<int:pk>/edit/', views.stratigraphic_qualifier_edit, name='stratigraphic-qualifier-edit'),
    path('rnames/structured_names', views.structuredname_list, name='structuredname-list'),
    path('rnames/structured_name/new', views.structuredname_new, name='structuredname-new'),
    path('rnames/structured_name/<int:pk>/', views.structuredname_detail, name='structuredname-detail'),
    path('rnames/structured_name/<int:pk>/delete/', views.structuredname_delete.as_view(), name='structuredname-delete'),
    path('rnames/structured_name/<int:pk>/edit/', views.structuredname_edit, name='structuredname-edit'),
]

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
#urlpatterns = format_suffix_patterns(urlpatterns)
