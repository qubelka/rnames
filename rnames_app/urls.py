from django.urls import path
from . import views

urlpatterns = [
    path('', views.name_list, name='name_list'),
    path('name/<int:pk>/', views.name_detail, name='name_detail'),
    path('name/new', views.name_new, name='name_new'),
    path('name/<int:pk>/edit/', views.name_edit, name='name_edit'),
    path('qualifier/<int:pk>/', views.qualifier_detail, name='qualifier-detail'),
]
