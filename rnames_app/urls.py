from django.urls import path
from . import views

urlpatterns = [
    path('', views.name_list, name='name_list'),
]
