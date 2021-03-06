from django.shortcuts import render

from contents.utils.utils import get_categories
from goods.models import GoodsChannelGroup, GoodsChannel, GoodsCategory
# Create your views here.
from django.views import View
from collections import OrderedDict
from contents.models import ContentCategory, Content


class IndexView(View):
    '''首页广告'''

    def get(self, request):
        '''提供首页广告页面'''
        # 准备商品分类对应的字典
        categories = OrderedDict()
        # TODO 需要中重点复习的内容
        # # 查询并展示商品分类:37个一级类别
        # channels = GoodsChannel.objects.order_by('group_id', 'sequence')
        # # 遍历所有频道
        # for channel in channels:
        #     # 获取当前频道所在的组
        #     group_id = channel.group_id  # 当前组
        #     # 构造基本的数据框架:只有11个组
        #     if group_id not in categories:
        #         categories[group_id] = {'channels': [], 'sub_cats': []}
        #     cat1 = channel.category  # 当前频道的类别
        #     # 将cat1添加到channels
        #     categories[group_id]['channels'].append({
        #         'id': cat1.id,
        #         'name': cat1.name,
        #         'url': channel.url
        #     })
        #     # 查询二级和三级
        #     for cat2 in cat1.subs.all():  # 从一级类别找二级类别
        #         cat2.sub_cats = []  # 给二级类别添加一个保存三级类别的列表
        #         for cat3 in cat2.subs.all():  # 从二级类别找三级类别
        #             cat2.sub_cats.append(cat3)  # 将三级类别添加到二级类别sub_cats
        #
        #         # 将二级类别添加到一级类别的sub_cats
        #         categories[group_id]['sub_cats'].append(cat2)
        categories = get_categories()
        # TODO ！！！！！！[代码中的FastDFS启动的storage没有报错，图片也可以正常得到，但是python.manage.shell中创建client不能使用，未解决！]
        # 查询首页广告的数据
        # 查询所有广告的类别
        contents = OrderedDict()
        content_categories = ContentCategory.objects.all()
        for content_category in content_categories:
            contents[content_category.key] = content_category.content_set.filter(status=True).order_by(
                'sequence')  # 查询到未下架的广告并排序
        # 使用广告类别查询出该类别对应的所有广告内容
        # 构造上下文
        context = {
            'categories': categories,
            'contents': contents
        }
        return render(request, 'index.html', context=context)
