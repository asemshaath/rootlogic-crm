from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),  
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()), 
            ('data', data),
            ('page_number', self.page.number),     
            ('total_pages', self.page.paginator.num_pages) 
        ]))