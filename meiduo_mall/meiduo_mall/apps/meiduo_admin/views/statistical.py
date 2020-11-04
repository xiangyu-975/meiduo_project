from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.mixins import ListModelMixin

from goods.models import GoodsVisitCount
from meiduo_admin.serializers.statistical import GoodsVisitSerializer
from users.models import User
from django.utils import timezone
from rest_framework.response import Response


class UserTotalCountView(APIView):
    # GET /meiduo_admin/statistical/total_count
    # 只有管理员才能访问
    permission_classes = [IsAdminUser]

    def get(self, request):
        '''
        统计网站的总用户数
        1,查询数据库统计网站的总用户数
        2,返回响应数据
        '''
        # 1查询数据库统计网站的总用户数
        count = User.objects.count()
        # 2返回要响应数据
        # 年-月-日-时-分-秒
        now_date = timezone.now()
        response_data = {
            'count': count,
            # 年-月-日
            'date': now_date.date(),
        }
        return Response(response_data)


class UserDayIncrementView(APIView):
    # GET /meiduo_admin/statistical/day_increment
    # 只有管理员才能访问
    permission_classes = [IsAdminUser]

    def get(self, request):
        '''
        统计网站当天访问的总数
        1.查询数据库统计网站的日增用户数
        2.返回响应数据
        '''
        # 1.查询数据库统计网站的日增用户数
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        count = User.objects.filter(date_joined__gte=now_date).count()
        response_data = {
            'count': count,
            # 年月日
            'date': now_date.date()
        }
        return Response(response_data)


class UserDayActiveView(APIView):
    # GET /meiduo_admin/statistical/day_active
    # 只有管理员才能访问
    permission_classes = [IsAdminUser]

    def get(self, request):
        '''
        统计网站日活用户
        1.查询数据库统计网站日活用户
        2.返回响应数据
        '''
        # 1 查询数据库统计当天日活用户的总数
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        count = User.objects.filter(last_login__gte=now_date).count()
        response_data = {
            'count': count,
            # 年月日
            'date': now_date.date()
        }
        return Response(response_data)


class UserDayOrder(APIView):
    # GET /meiduo_admin/statistical/day_order
    # 只有管理员才能访问
    permission_classes = [IsAdminUser]

    def get(self, request):
        '''
        统计网站当天下单用户
        1.查询数据库统计当天下单用户
        2.返回响应数据
        '''
        # 查询数据库统计当天用户下单
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        # user
        count = User.objects.filter(orders__create_time__gte=now_date).distinct().count()
        # 返回响应数据
        response_data = {
            'count': count,
            'date': now_date.date()
        }
        return Response(response_data)


class UserMonthIncrementView(APIView):
    # GET /meiduo_admin/statistical/month_increment
    # 管理员才能登陆
    permission_classes = [IsAdminUser]

    def get(self, request):
        '''
        统计网站30天每日新增用户数量
        1.查询30天每天用户新增的数量
        2.返回响应数据
        '''
        # 结束时间
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        # 起始时间:now_time - 29
        begin_date = now_date - timezone.timedelta(days=29)
        # 当天日期
        current_date = begin_date
        # 新增用户的数量
        month_li = []
        while current_date <= now_date:
            # 次日时间
            next_date = current_date + timezone.timedelta(days=1)
            # 统计当天用户新增的数量
            count = User.objects.filter(date_joined__gte=current_date, date_joined__lt=next_date).count()
            month_li.append({
                'count': count,
                'date': current_date.date()
            })
            current_date += timezone.timedelta(days=1)
        # 返回响应数据
        return Response(month_li)


# class GoodsDayViewsView(APIView):
#     # GET /meiduo_admin/statistical/good_day_views
#     # 只有管理员才能访问
#     permission_classes = [IsAdminUser]
#
#     def get(self, request):
#         '''
#         获取日分类访问量的数据
#         1.查询获取当天日分类化商品的数据
#         2.将数据序列化返回
#         '''
#         now_date = timezone.now().date()
#         good_visits = GoodsVisitCount.objects.filter(date=now_date)
#         # 将查到的数据序列化并返回
#         serializer = GoodsVisitSerializer(good_visits, many=True)
#         return Response(serializer.data)
class GoodsDayViewsView(ListAPIView):
    # GET /meiduo_admin/statistical/good_day_views
    # 只有管理员才能访问
    permission_classes = [IsAdminUser]
    serializer_class = GoodsVisitSerializer

    # queryset = GoodsVisitCount.objects.filter(date=now_date)
    def get_queryset(self):
        now_date = timezone.now().date()
        queryset = GoodsVisitCount.objects.filter(date=now_date)
        return queryset

    # def get(self, request):
    #     return self.list(request)

        # def get(self, request):
        #     '''
        #     获取日分类访问量的数据
        #     1.查询获取当天日分类化商品的数据
        #     2.将数据序列化返回
        #     '''
        #     good_visits = self.get_queryset()
        #     # 将查到的数据序列化并返回
        #     serializer = self.get_serializer(good_visits, many=True)
        #     return Response(serializer.data)
