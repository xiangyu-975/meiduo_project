import pickle, base64
from django_redis import get_redis_connection


def merge_carts_cookies_redis(request, user, response):
    '''合并购物车'''
    # 获取cookies中的购物车数据
    cart_str = request.COOKIES.get('carts')
    # 判断cookies中购物车数据是否存在
    if not cart_str:
        return response
    # 将cart_str转为bytes类型的字符串
    cookie_cart_str_bytes = cart_str.encode()
    # 将bytes类型的字符串转bytes类型的字典
    cookie_cart_dict_bytes = base64.b64decode(cookie_cart_str_bytes)
    # 将bytes的字典转化为真正的字典
    cookie_cart_dict = pickle.loads(cookie_cart_dict_bytes)
    # 如果存在，需要合并

    # 准备新的数据容器,保存新的sku_id:count,selected,unselected
    new_cart_dict = {}
    new_selected_add = []
    new_selected_rem = []
    # 遍历出cookies中的购物车数据
    for sku_id, cookie_dict in cookie_cart_dict.items():
        # new_cart_dict[sku_id] = {
        #     'count': cookie_dict['count'],
        # }
        new_cart_dict[sku_id] = cookie_dict['count']
        if cookie_dict['selected']:
            new_selected_add.append(sku_id)
        else:
            new_selected_rem.append(sku_id)

    # 根据新的数据结构,合并到redis
    redis_conn = get_redis_connection('carts')
    pl = redis_conn.pipeline()
    pl.hmset('carts_%s' % user.id, new_cart_dict)
    if new_selected_add:
        pl.sadd('selected_%s' % user.id, *new_selected_add)
    if new_selected_rem:
        pl.srem('selected_%s' % user.id, *new_selected_rem)
    pl.execute()
    # 删除cookies
    response.delete_cookie('carts')
    return response
