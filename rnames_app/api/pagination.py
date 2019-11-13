from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
    )

class ReferenceLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 4
    max_limit = 10

class ReferencePageNumberPagination(PageNumberPagination):
    page_size = 3

class RelationPageNumberPagination(PageNumberPagination):
    page_size = 500
