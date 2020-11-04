from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView, ListCreateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from meiduo_admin.serializers.users import AdminAuthSerializer, UserInfoSerializer
from users.models import User


class AdminAuthView(CreateAPIView):
    serializer_class = AdminAuthSerializer


# class AdminAuthView(APIView):
#     def post(self, request):
#         '''
#         管理员登陆
#         1,获取参数并进行校验(参数完整性,用户名密码是否正确)
#         2,创建jwt token保存登陆用户身份信息
#         3,返回响应数据
#         '''
#         # 获取参数并进行校验
#         serializer = AdminAuthSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # 创建jwt_token保存登陆用户的身份信息
#         serializer.save()  # 调用序列化器create
#
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# GET /meiduo_admin/users/?keyword=<关键字>
# class UserInfoView(APIView):
#     permission_classes = [IsAdminUser]
#
#     def get(self, request):
#         '''
#         获取网站的普通用户的数据
#         1.查询获取普通用户的数据
#             1.1如果传递信息中有keyword,那么返回带有keyword的用户信息
#             1.2如果没有,那么返回所有的用户信息
#         2.将普通用户的数据序列化并返回
#         '''
#         keyword = request.query_params.get('keyword')
#         if keyword:
#             users = User.objects.filter(username__contains=keyword, is_staff=False)
#         else:
#             users = User.objects.filter(is_staff=False)
#         # 2.将普通用户序列化返回
#         serializer = UserInfoSerializer(users, many=True)
#         return Response(serializer.data)
# class UserInfoView(ListAPIView):
class UserInfoView(ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserInfoSerializer

    def get_queryset(self):
        '''
        self.request 请求对象
        :return:
        '''
        keyword = self.request.query_params.get('keyword')
        if keyword:
            users = User.objects.filter(username__contains=keyword, is_staff=False)
        else:
            users = User.objects.filter(is_staff=False)
        return users

    # def get(self, request):
    #     return self.list(request)

    # def get(self, request):
    #     '''
    #     获取网站的普通用户的数据
    #     1.查询获取普通用户的数据
    #         1.1如果传递信息中有keyword,那么返回带有keyword的用户信息
    #         1.2如果没有,那么返回所有的用户信息
    #     2.将普通用户的数据序列化并返回
    #     '''
    #
    #     users = self.get_queryset()
    #     # 2.将普通用户序列化返回
    #     serializer = self.get_serializer(users, many=True)
    #     return Response(serializer.data)
    # def post(self, request):
    #     '''
    #     保存新增用户数据
    #     1.获取参数并校验(完整性,是否已经注册(手机号,用户名)手机号格式,邮箱格式)
    #     2.保存新增数据
    #     3.序列化新增数据并返回
    #     '''
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     # 保存新增数据
    #     serializer.save()  # 调用序列化器类create
    #     # 将新增用户数据序列化并返回
    #     return Response(serializer.data,status=status.HTTP_201_CREATED)
    # def post(self, request):
    #     return self.create(request)
