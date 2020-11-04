from django.conf.urls import url

from meiduo_admin.views import orders
from meiduo_admin.views import users, statistical, channels, skus, spus

urlpatterns = [
    # 进行url配置
    url(r'^authorizations/$', users.AdminAuthView.as_view()),
    # 数据统计
    url(r'^statistical/total_count/$', statistical.UserTotalCountView.as_view()),
    url(r'^statistical/day_increment/$', statistical.UserDayIncrementView.as_view()),
    url(r'^statistical/day_active/$', statistical.UserDayActiveView.as_view()),
    url(r'^statistical/day_orders/$', statistical.UserDayOrder.as_view()),
    url(r'^statistical/month_increment/$', statistical.UserMonthIncrementView.as_view()),
    url(r'^statistical/goods_day_views/$', statistical.GoodsDayViewsView.as_view()),

    # 用户管理
    url(r'^users/$', users.UserInfoView.as_view()),
    # 频道管理
    url(r'^goods/channel_types/$', channels.ChannelTypesView.as_view()),
    url(r'^goods/categories/$', channels.ChannelCategoriesView.as_view()),
    # 图片管理
    url(r'^skus/simple/$', skus.SKUSimpleView.as_view()),
    # SPU管理
    url(r'^goods/simple/$', spus.SPUSimpleView.as_view()),
    url(r'^goods/(?P<pk>\d+)/specs/$', spus.SPUSpecView.as_view()),
]

# 频道管理
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('goods/channels', channels.ChannelViewSet, basename='channels')
urlpatterns += router.urls
# 商品sku管理
router = DefaultRouter()
router.register('skus/images', skus.SKUImageViewSet, basename='images')
urlpatterns += router.urls
# SKU管理
router = DefaultRouter()
router.register('skus', skus.SKUViewSet, basename='skus')
urlpatterns += router.urls
# 订单管理
router = DefaultRouter()
router.register('orders', orders.OrderViewSet, basename='orders')
urlpatterns += router.urls
