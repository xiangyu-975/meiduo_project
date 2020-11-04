from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from goods.models import SPU, SPUSpecification
from meiduo_admin.serializers.spus import SPUSimpleSerializer, SPUSpecSerializer


# GET /meiduo_admin/goods/simple/
class SPUSimpleView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = SPU.objects.all()
    serializer_class = SPUSimpleSerializer
    # 关闭分页
    pagination_class = None


# GET /meiduo_admin/goods/(?P<pk>\d+)/specs/
class SPUSpecView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = SPUSpecSerializer

    # queryset = SPUSpecification.objects.filter(spu_id=pk)

    def get_queryset(self):
        '''
        self.kwargs: 字典,保存从url地址中提取的所有命名参数
        :return:
        '''
        pk = self.kwargs['pk']
        return SPUSpecification.objects.filter(spu_id=pk)
    # 关闭分页
    pagination_class = None

    # def get(self, request):
    #     return self.list(request)  # 会调用分页

    # def get(self, request, pk):
    #     '''
    #     查询spu商品规格数据
    #     1.查询获取spu商品的规格数据
    #     2.将spu商品的规格数据序列化返回
    #     '''
    #     # 1.查询获取spu商品的规格数据
    #     specs = self.get_queryset()
    #     # 2.将spu商品的规格数据序列化并返回
    #     serializer = self.get_serializer(specs, many=True)
    #     return Response(serializer.data)

# class SPUSpecView(APIView):
#     permission_classes = [IsAdminUser]
#
#     def get(self, request, pk):
#         '''
#         查询spu商品规格数据
#         1.查询获取spu商品的规格数据
#         2.将spu商品的规格数据序列化返回
#         '''
#         # 1.查询获取spu商品的规格数据
#         specs = SPUSpecification.objects.filter(spu_id=pk)
#         # 2.将spu商品的规格数据序列化并返回
#         serializer = SPUSpecSerializer(specs,many=True)
#         return Response(serializer.data)
