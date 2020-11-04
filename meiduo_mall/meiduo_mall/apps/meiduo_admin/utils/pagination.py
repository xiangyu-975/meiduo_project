from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


# 分页<page>页容量<page_size>



class StandardResultPagination(PageNumberPagination):
    # 分页时默认的页容量
    page_size = 5
    # 获取分页数据时,传递页容量参数的名称
    page_size_query_param = 'pagesize'
    max_page_size = 20

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('counts', self.page.paginator.count),
            ('lists', data),
            ('page', self.page.number),
            ('pages', self.page.paginator.num_pages),
            ('pagesize', self.get_page_size(self.request)),
        ]))
