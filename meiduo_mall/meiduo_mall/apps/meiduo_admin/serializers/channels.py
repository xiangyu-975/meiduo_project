from rest_framework import serializers

from goods.models import GoodsChannel, GoodsChannelGroup, GoodsCategory


class ChannelSerializer(serializers.ModelSerializer):
    '''频道的序列化器类'''
    group_id = serializers.IntegerField(label='频道组的ID')
    category_id = serializers.IntegerField(label='一级分类的ID')
    # 关联对象的嵌套序列化
    group = serializers.StringRelatedField(label='频道组')
    category = serializers.StringRelatedField(label='一级分类')

    class Meta:
        model = GoodsChannel
        exclude = ('create_time', 'update_time')

    def validate_group_id(self, value):
        # 校验频道组是否存在
        try:
            group = GoodsChannelGroup.objects.get(id=value)
        except GoodsChannelGroup.DoesNotExist:
            raise serializers.ValidationError('频道组不存在')
        return value

    def validate_category_id(self, value):
        try:
            category = GoodsCategory.objects.get(id=value, parent=None)
        except GoodsCategory.DoesNotExist:
            raise serializers.ValidationError('一级分类不存在')
        return value


class ChannelTypeSerializer(serializers.ModelSerializer):
    '''频道组的序列化器类'''

    class Meta:
        model = GoodsChannelGroup
        fields = ('id', 'name')


class ChannelCategorySerializer(serializers.ModelSerializer):
    '''分类的序列化器类'''

    class Meta:
        model = GoodsCategory
        fields = ('id', 'name')
