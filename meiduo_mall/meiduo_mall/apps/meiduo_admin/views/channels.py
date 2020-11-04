from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser

from goods.models import GoodsChannel, GoodsChannelGroup, GoodsCategory
from meiduo_admin.serializers.channels import ChannelSerializer, ChannelTypeSerializer, ChannelCategorySerializer


class ChannelViewSet(ModelViewSet):
    '''频道管理视图集'''
    permission_classes = [IsAdminUser]
    # 指定视图所需要的查询集
    queryset = GoodsChannel.objects.all()
    # 指定视图所使用的序列化器类
    serializer_class = ChannelSerializer
    '''
        GET /meiduo_admin/goods/channels/  --> list
        POST /meiduo_admin/goods/channels/ --> create
        GET /meiduo_admin/goods/channels/(?P<pk>\d+)/ --> retrieve
        PUT /meiduo_admin/goods/channels/(?P<pk>\d+)/ --> update
        DELETE /meiduo_admin/goods/channels/(?P<pk>\d+)/ --> destroy
    '''
    # GET /meiduo_admin/goods/channels --> list
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()  # 调用序列化器类中的create
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
    #
    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance,data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()  # 调用序列化器中的update
    #     return Response(serializer.data)
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.delete()
    #     return Response(status.HTTP_204_NO_CONTENT)


class ChannelTypesView(ListAPIView):
    # GET /meiduo_admin/goods/channel_types/
    permission_classes = [IsAdminUser]
    serializer_class = ChannelTypeSerializer
    queryset = GoodsChannelGroup.objects.all()

    # 关闭分页
    pagination_class = None

    # def get(self, request):
    #     return self.list(request)

    # def get(self, request):
    #     '''
    #     获取所有频道组的数据
    #     1.查询获取所有频道组的数据
    #     2.将频道组的数据序列化并返回
    #     '''
    #     # 查询所有频道组的数据
    #     groups = self.queryset()
    #     # 频道组数据序列化返回
    #     serializer = ChannelTypeSerializer(groups,many=True)
    #     return Response(serializer.data)


class ChannelCategoriesView(ListAPIView):
    # GET /meiduo_admin/goods/categories/
    permission_classes = [IsAdminUser]
    serializer_class = ChannelCategorySerializer
    queryset = GoodsCategory.objects.filter(parent=None)

    # 关闭分页
    pagination_class = None
