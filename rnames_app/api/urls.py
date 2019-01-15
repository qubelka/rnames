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
    )

urlpatterns = [
#    re_path('api/getNames/$', NameList.as_view(), name='NameList'),
#    path('api/getName/<int:pk>/', views.NameDetail.as_view(), name='NameDetail'),
    url('api/references/$', ReferenceListAPIView.as_view(), name='list'),
    path('api/references/create/', ReferenceCreateAPIView.as_view(), name='create'),
    path('api/reference/<int:pk>/', ReferenceDetailAPIView.as_view(), name='detail'),
    path('api/reference/<int:pk>/delete/', ReferenceDeleteAPIView.as_view(), name='delete'),
    path('api/reference/<int:pk>/update/', ReferenceUpdateAPIView.as_view(), name='update'),
#    re_path('api/getNames/$', NameList.as_view(), name='NameList'),
]

#urlpatterns = format_suffix_patterns(urlpatterns)
