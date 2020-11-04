from django.conf import settings
from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from rest_framework.exceptions import APIException


class FastDFSStorage(Storage):
    '''自定义文件的存储类'''

    # 文件存储类的初始化方法
    def __init__(self, client_conf=None, fdfs_base_url=None):
        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONF
        # 保存客户端配置文件路径
        self.client_conf = client_conf
        # if not fdfs_base_url:
        #     self.fdfs_base_url = settings.FDFS_BASE_URL
        # self.fdfs_base_url = fdfs_base_url
        # 保存的是FDFS nginx的地址
        self.fdfs_base_url = fdfs_base_url or settings.FDFS_BASE_URL

    def _open(self, name, mode='rb'):
        '''打开文件时会被调用的：必须重写'''
        # 因为当前不是去打开某一个文件，所以这个方法目前无用，但是有必须重写，所以pass，做文件的下载
        pass

    def _save(self, name, content):
        '''
        PS：将来在后台管理系统中，需要在这个方法中实现文件上传到FDFS服务器
        保存文件时会被调用的：文档告诉我必须重写
        :param name: 文件路径
        :param content: 文件二进制内容
        :return: None
        '''
        # 创建客户端对象
        client = Fdfs_client(self.client_conf)
        # 上传文件到fdfs系统
        res = client.upload_by_buffer(content.read())
        if res.get('Status') != 'Upload successed.':
            raise APIException('上传文件失败')
        # 获取文件的id
        file_id = res.get('Remote file_id')
        return file_id
        # 因为当前不是去保存文件，所以这个方法目前无用，必须重写

    def exists(self, name):
        '''
        判断上传的文件名称和系统中原有的文件名是否冲突
        :param name: 上传的文件名
        '''
        return False

    def url(self, name):
        '''
        返回文件的全路径
        :param name: 文件的相对路径
        :return: http://192.168.103.158:8888/group1/M00/00/00/wKhnnlxw_gmAcoWmAAEXU5wmjPs35.jpeg
        '''
        # return 'http://192.168.220.128:8888/' + name
        return self.fdfs_base_url + name
