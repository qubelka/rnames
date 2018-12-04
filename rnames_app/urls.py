from django.urls import path
from . import views

urlpatterns = [
    path('', views.name_list, name='name_list'),
    path('name/<int:pk>/', views.name_detail, name='name_detail'),
]
