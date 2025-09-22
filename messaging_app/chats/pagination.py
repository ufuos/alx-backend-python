from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MessagePagination(PageNumberPagination):
    # Default page size
    page_size = 20
    # Allow clients to override with ?page_size=...
    page_size_query_param = 'page_size'
    # Maximum items per page allowed
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            "count": self.page.paginator.count,           # total number of items
            "total_pages": self.page.paginator.num_pages, # total number of pages
            "current_page": self.page.number,             # current page number
            "page_size": self.get_page_size(self.request) or self.page_size,
            "results": data
        })
