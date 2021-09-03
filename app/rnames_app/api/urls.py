from django.conf.urls import url
from django.contrib import admin
from django.urls import path #, re_path
#from rnames_app.api.views import NameList
#from rest_framework.urlpatterns import format_suffix_patterns

from .views import(
    ReferenceCreateAPIView,
    ReferenceDeleteAPIView,
    ReferenceDetailAPIView,
    ReferenceListAPIView,
    ReferenceUpdateAPIView,
    RelationListAPIView,
    )

urlpatterns = [
#    re_path('api/getNames/$', NameList.as_view(), name='NameList'),
#    path('api/getName/<int:pk>/', views.NameDetail.as_view(), name='NameDetail'),
    url('rnames/api/references/$', ReferenceListAPIView.as_view(), name='list'),
    path('rnames/api/references/create/', ReferenceCreateAPIView.as_view(), name='create'),
    path('rnames/api/reference/<int:pk>/', ReferenceDetailAPIView.as_view(), name='detail'),
    path('rnames/api/reference/<int:pk>/delete/', ReferenceDeleteAPIView.as_view(), name='delete'),
    path('rnames/api/reference/<int:pk>/update/', ReferenceUpdateAPIView.as_view(), name='update'),
    url('rnames/api/relations/$', RelationListAPIView.as_view(), name='list'),
#    re_path('api/getNames/$', NameList.as_view(), name='NameList'),
]

#urlpatterns = format_suffix_patterns(urlpatterns)
