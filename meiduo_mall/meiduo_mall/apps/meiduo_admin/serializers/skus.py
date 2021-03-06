from django.db import transaction
from rest_framework import serializers

from goods.models import SKUImage, SKU, SKUSpecification, SPU, SpecificationOption


class SKUImageSerializer(serializers.ModelSerializer):
    '''sku图片序列化器类'''
    sku_id = serializers.IntegerField(label='sku商品的id')
    sku = serializers.StringRelatedField(label='sku商品')

    class Meta:
        model = SKUImage
        exclude = ('create_time', 'update_time')

    def validate_sku_id(self, value):
        # 校验sku商品是否存在
        try:
            sku = SKU.objects.get(id=value)
        except SKU.DoesNotExist:
            raise serializers.ValidationError('商品不存在')
        return value

    def create(self, validated_data):
        # 添加图片
        sku_image = super().create(validated_data)
        # 设置默认图片
        sku = sku_image.sku
        if not sku_image:
            sku.default_image = sku_image.image
            sku.save()
        return sku_image


class SKUSimpleSerializer(serializers.ModelSerializer):
    '''SKU商品序列化器类'''

    class Meta:
        model = SKU
        fields = ('id', 'name')


class SKUSpecSerializer(serializers.ModelSerializer):
    '''SKU的具体规格序列化器类'''
    spec_id = serializers.IntegerField(label='规格id')
    option_id = serializers.IntegerField(label='选项id')

    class Meta:
        model = SKUSpecification
        fields = ('spec_id', 'option_id')


class SKUSerializer(serializers.ModelSerializer):
    '''商品的序列化器类'''
    category = serializers.StringRelatedField(label='分类')
    spu_id = serializers.IntegerField(label='SPU ID')
    specs = SKUSpecSerializer(label='具体规格', many=True)

    class Meta:
        model = SKU
        exclude = ('create_time', 'update_time', 'spu', 'comments', 'default_image')
        extra_kwargs = {
            'sales': {
                'read_only': True
            }
        }

    def validate(self, attrs):
        # 1.spu是否存在
        spu_id = attrs['spu_id']
        try:
            spu = SPU.objects.get(id=spu_id)
        except SPU.DoesNotExist:
            raise serializers.ValidationError('SPU不存在')
        attrs['category_id'] = spu.category3.id
        # 2.spu数据是否合法
        # 检验spu规格数量是否合法
        specs = attrs['specs']
        spu_specs = spu.specs.all()
        specs_count = len(specs)
        spu_specs_count = spu_specs.count()
        if specs_count != spu_specs_count:
            raise serializers.ValidationError('规格数据有误')
        # 检验spu规格数据是否合法
        spec_ids = [spec.get('spec_id') for spec in specs]
        spu_spec_ids = [spec.id for spec in spu_specs]
        # 排序
        spec_ids.sort()
        spu_spec_ids.sort()
        # 校验
        if spec_ids != spu_spec_ids:
            raise serializers.ValidationError('规格数据有误')
        # 3.规格选项数据是否合法
        for spec in specs:
            # 获取spec_id和option_id
            spec_id = spec.get('spec_id')
            option_id = spec.get('option_id')

            # 校验选项数据是否合法
            options = SpecificationOption.objects.filter(spec_id=spec_id)
            option_ids = [option.id for option in options]
            if option_id not in option_ids:
                raise serializers.ValidationError('选项数据有误')
        return attrs

    def create(self, validated_data):
        specs = validated_data.pop('specs')
        with transaction.atomic():
            # 添加sku商品数据
            sku = SKU.objects.create(**validated_data)
            # 添加sku具体商品数据
            for spec in specs:
                # 获取spec_id和option_id
                spec_id = spec.get('spec_id')
                option_id = spec.get('option_id')

                SKUSpecification.objects.create(
                    sku=sku,
                    spec_id=spec_id,
                    option_id=option_id
                )

        return sku

    def update(self, instance, validated_data):
        specs = validated_data.pop('specs')
        with transaction.atomic():
            # 更新sku的数据
            super().update(instance, validated_data)
            # 更新sku的规格数据
            instance.specs.all().delete()
            for spec in specs:
                # 获取spec_id和option_id
                spec_id = spec.get('spec_id')
                option_id = spec.get('option_id')

                SKUSpecification.objects.create(
                    sku=instance,
                    spec_id=spec_id,
                    option_id=option_id
                )
        return instance
