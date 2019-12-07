# rnames_app/api
from django.db.models import Q

from rest_framework.filters import (
        SearchFilter,
        OrderingFilter,
    )

from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView
    )

#from rest_framework.pagination import (
#    LimitOffsetPagination,
#    PageNumberPagination
#    )

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    )

from rnames_app.models import Reference, Relation, Name

from .pagination import ReferencePageNumberPagination, ReferenceLimitOffsetPagination
#, RelationPageNumberPagination

from .permissions import IsOwnerOrReadOnly

from .serializers import (
    ReferenceCreateUpdateSerializer,
    ReferenceDetailSerializer,
    ReferenceListSerializer,
    RelationListSerializer,
    )

class ReferenceCreateAPIView(CreateAPIView):
    queryset = Reference.objects.get_queryset().filter(is_active=True)
    serializer_class = ReferenceCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
#    def perform_create(self, serializer):
#        serializer.save(created_by=self.request.user, title='My Title')
#        email send_email
class ReferenceDeleteAPIView(DestroyAPIView):
    queryset = Reference.objects.get_queryset().filter(is_active=True)
    serializer_class = ReferenceDetailSerializer

class ReferenceDetailAPIView(RetrieveAPIView):
    queryset = Reference.objects.get_queryset().filter(is_active=True)
    serializer_class = ReferenceDetailSerializer

class ReferenceListAPIView(ListAPIView):
#   commented as there is the def get_queryset
#    queryset = Reference.objects.get_queryset().filter(is_active=True)
    serializer_class = ReferenceListSerializer
    filter_backends= [SearchFilter, OrderingFilter]
#   use the ?search= for these fields in the URL
    search_fields = ['title', 'modified_by__first_name', 'modified_by__last_name']
#   use the ?limit=2&offset=10 style for LimitOffsetPagination
    pagination_class = ReferencePageNumberPagination #ReferenceLimitOffsetPagination #LimitOffsetPagination #PageNumberPagination #PostPageNumberPagination

#    permission_classes = (IsAdminUser,)
    def get_queryset(self, *args, **kwargs):
        #queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
#        queryset_list = Post.objects.all() #filter(user=self.request.user)
#        queryset_list = Reference.objects.get_queryset().filter(is_active=True)
        queryset_list = Reference.objects.select_related('created_by', 'modified_by').filter(is_active=True)

#   use the ?q= for these fields in the URL
#   you can also use the ?search=xxx&q= for these fields in the URL
#   you can use the &ordering=-title etc. for ordering the list by descendinf title
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                    Q(title__icontains=query)|
#                    Q(content__icontains=query)|
#                    Q(user__first_name__icontains=query) |
                    Q(created_by__last_name__icontains=query)
                    ).distinct()
        return queryset_list

class ReferenceUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Reference.objects.get_queryset().filter(is_active=True)
    serializer_class = ReferenceCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

#    def perform_update(self, serializer):
#        serializer.save(created_by=self.request.user, title='My Title')


#from rest_framework.views import APIView
#from rest_framework.response import Response
#from rest_framework import status, generics
#from .serializers import NameSerializer
#from rnames_app.models import Name
#from rnames_app.filters import NameFilter
#from .filters import UserFilter, APINameFilter


# To make another field as a pk
# lookup_field = 'slug'
# in urls you set 'abc'
# lookup_url_kwarg = 'abc'


#class NameList(generics.ListAPIView):
#    serializer_class = NameSerializer

#    def get_queryset(self, request):
#        names = Name.objects.is_active()
#        queryset = Name.objects.all()
#        filter_fields = ('category', 'in_stock')

#        name_filter = NameFilter(request.GET, queryset=names)
#        serializer = NameSerializer(name_filter, many=True)
#        serializer = NameSerializer(queryset, many=True)
#        return Response(serializer.data)

#    def post(self):
#        pass

# Lists all Names or create a new one
# getNames/ the URL
#class NameDetail(APIView):

#    def get(self, request, pk):
#        names = Name.objects.is_active().get(pk=pk)
#        serializer = NameSerializer(names, many=False)
#        return Response(serializer.data)

#    def post(self):
#        pass

#def user_search(request):
#    user_list = User.objects.all()
#    user_filter = UserFilter(request.GET, queryset=user_list)
#    return render(request, 'rnames_app/user_list.html', {'filter': user_filter})

class RelationListAPIView(ListAPIView):
#   commented as there is the def get_queryset
#    queryset = Reference.objects.get_queryset().filter(is_active=True)
    serializer_class = RelationListSerializer
#    filter_backends= [SearchFilter, OrderingFilter]

#    search_fields = ['name_one', 'name_two',]
#    pagination_class = RelationPageNumberPagination

#    permission_classes = (IsAdminUser,)
    def get_queryset(self, *args, **kwargs):
#        queryset_list = Relation.objects.get_queryset().filter(is_active=True).filter(reference__is_active=True).filter(name_one__qualifier__is_active=True).filter(name_two__qualifier__is_active=True).filter(name_one__location__is_active=True).filter(name_two__location__is_active=True).filter(name_one__name__is_active=True).filter(name_two__name__is_active=True).filter(name_one__is_active=True).filter(name_two__is_active=True)
#        queryset_list = Relation.objects.prefetch_related('reference','name_one','name_two', 'created_by', 'modified_by').filter(is_active=True).filter(reference__is_active=True).filter(name_one__qualifier__is_active=True).filter(name_two__qualifier__is_active=True).filter(name_one__location__is_active=True).filter(name_two__location__is_active=True).filter(name_one__name__is_active=True).filter(name_two__name__is_active=True).filter(name_one__is_active=True).filter(name_two__is_active=True)
#        queryset_list = Relation.objects.select_related('reference','name_one','name_two', 'created_by', 'modified_by').filter(is_active=True).filter(reference__is_active=True).filter(name_one__qualifier__is_active=True).filter(name_two__qualifier__is_active=True).filter(name_one__location__is_active=True).filter(name_two__location__is_active=True).filter(name_one__name__is_active=True).filter(name_two__name__is_active=True).filter(name_one__is_active=True).filter(name_two__is_active=True)
#        queryset_list = Relation.objects.select_related('reference')\
#                                        .select_related('name_one')\
#                                        .select_related('name_two')\
#                                        .select_related('created_by')\
#                                        .select_related('modified_by')\
#                                        .filter(is_active=True).filter(reference__is_active=True).filter(name_one__qualifier__is_active=True).filter(name_two__qualifier__is_active=True).filter(name_one__location__is_active=True).filter(name_two__location__is_active=True).filter(name_one__name__is_active=True).filter(name_two__name__is_active=True).filter(name_one__is_active=True).filter(name_two__is_active=True)
        queryset_list = Relation.objects.all().values(
            'id',
#            'reference',
            'name_one__location__name',
            'name_one__name__name',
            'name_one__qualifier__level',
            'name_one__qualifier__qualifier_name__name',
            'name_one__qualifier__stratigraphic_qualifier__name',
            'name_two__location__name',
            'name_two__name__name',
            'name_two__qualifier__level',
            'name_two__qualifier__qualifier_name__name',
            'name_two__qualifier__stratigraphic_qualifier__name',
            'belongs_to')

#        queryset_list = Relation.objects.select_related('reference').all()
#        queryset_list = Relation.objects.select_related('reference','name_one','name_two', 'created_by', 'modified_by').filter(is_active=True)
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                    Q(created_by__icontains=query)|
                    Q(created_by__last_name__icontains=query)
                    ).distinct()
        return queryset_list
