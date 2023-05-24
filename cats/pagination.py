# cats/pagination.py
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CatsPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'Response': data
        })