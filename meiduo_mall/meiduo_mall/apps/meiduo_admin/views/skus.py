from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from django.db.models import Q

from goods.models import SKUImage, SKU
from meiduo_admin.serializers.skus import SKUImageSerializer, SKUSimpleSerializer, SKUSerializer


class SKUImageViewSet(ModelViewSet):
    '''sku图片的视图集'''
    permission_classes = [IsAdminUser]
    queryset = SKUImage.objects.all()
    serializer_class = SKUImageSerializer

    # GET /meiduo_admin/skus/images/  -> list
    # POST /meiduo_admin/skus/images/ -> create
    # GET /meiduo_admin/skus/images/(?P<pk>\d+)/ -> retrieve
    # PUT /meiduo_admin/skus/images/(?P<pk>\d+)/ -> update
    # DELETE /meiduo_admin/skus/images/(?P<pk>\d+)/ -> destroy

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()  # 调用序列化器中的create
    #     return Response(serializer.data,status=201)
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()  # 调用序列化器的create方法
    #     return Response(serializer.data)
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.delete()
    #     return Response(status=204)


# API: GET /meiduo_admin/skus/simple
class SKUSimpleView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = SKU.objects.all()
    serializer_class = SKUSimpleSerializer

    # 关闭分页
    pagination_class = None


# GET /meiduo_admin/skus/?keyword=<名称|副标题>&page=<页码>&page_size=<页容量>
class SKUViewSet(ModelViewSet):
    '''sku的视图集'''
    permission_classes = [IsAdminUser]

    # GET /meiduo_admin/skus/ -> list
    def get_queryset(self):
        # 获取keyword
        keyword = self.request.query_params.get('keyword')
        if keyword:
            # 根据keyword查询名称或副标题中含有keyword的商品
            skus = SKU.objects.filter(Q(name__contains=keyword) | Q(caption__contains=keyword))
        else:
            # 获取所有的商品
            skus = SKU.objects.all()
        return skus

    serializer_class = SKUSerializer

    # 指定router动态生成路由时，提取参数的正则表达式
    # lookup_value_regex = '\d+'
    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset,many=True)
    #     return Response(serializer.data)

    # POST /meiduo_admin/skus/ -> create
    # GET /meiduo_admin/skus/(?P<pk>\d+)/ -> retrieve
    # PUT /meiduo_admin/skus/(?P<pk>\d+)/ -> update
    # DELETE /meiduo_admin/skus/(?P<pk>\d+)/ -> delete
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data,status=201)
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()  # 调用序列化器类中的update
    #     return Response(serializer.data)
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.delete()
    #     return Response(status=204)
