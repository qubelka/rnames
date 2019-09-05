from django.conf.urls import url
from django.urls import path, re_path
from . import views
#from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('rnames/', views.name_list, name='name_list'),
    path('rnames/name/<int:pk>/', views.name_detail, name='name_detail'),
    path('rnames/name/new', views.name_new, name='name_new'),
    path('rnames/name/<int:pk>/edit/', views.name_edit, name='name_edit'),
    path('rnames/qualifier/<int:pk>/', views.qualifier_detail, name='qualifier-detail'),
    url(r'^search/$', views.user_search, name='user_search'),
]

#urlpatterns = format_suffix_patterns(urlpatterns)
