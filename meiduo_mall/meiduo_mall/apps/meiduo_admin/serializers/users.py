import re
from django.utils import timezone

from rest_framework import serializers

from users.models import User


class AdminAuthSerializer(serializers.ModelSerializer):
    '''管理员登陆序列化器类'''
    token = serializers.CharField(label='jwt token', read_only=True)
    username = serializers.CharField(label='用户名')

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'token')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        # 用户名和密码是否正确
        username = attrs['username']
        password = attrs['password']
        try:
            user = User.objects.get(username=username, is_staff=True)
        except User.DoesNotExist:
            raise serializers.ValidationError('用户名或密码错误')
        else:
            # 校验密码
            if not user.check_password(password):
                raise serializers.ValidationError('用户名或密码错误')

            # 给attrs中添加user属性，保存登录用户
            attrs['user'] = user

        return attrs

    def create(self, validated_data):
        # 获取登录用户user
        user = validated_data['user']

        # 设置最新登录时间
        user.last_login = timezone.now()
        user.save()

        # 服务器生成jwt token, 保存当前用户的身份信息
        from rest_framework_jwt.settings import api_settings

        # 组织payload数据的方法
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        # 生成jwt token数据的方法
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        # 组织payload数据
        payload = jwt_payload_handler(user)
        # 生成jwt token
        token = jwt_encode_handler(payload)

        # 给user对象增加属性，保存jwt token的数据
        user.token = token

        return user


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # 自动生成的id是默认read_only=True
        fields = ('id', 'username', 'mobile', 'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate_mobile(self, value):
        # 手机号格式
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        # 手机号是否注册
        count = User.objects.filter(mobile=value).count()
        if count > 0:
            raise serializers.ValidationError('手机号已注册')
        return value

    # User.objects.create(**validated_data)
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
