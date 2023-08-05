import os

from adapay.request_tools import request_post, request_get, corp_member_create, corp_member_query


class CorpMember(object):

    @classmethod
    def create(cls, **kwargs):
        """
        创建企业用户
        """
        file_path = kwargs.get('attach_file')
        files = {'attach_file': (os.path.basename(file_path), open(file_path, 'rb'), 'application/octet-stream')}
        kwargs.pop('attach_file')
        return request_post(corp_member_create, kwargs, files)

    @classmethod
    def query(cls, **kwargs):
        """
        查询企业用户
        """
        url = corp_member_query.format(member_id=kwargs.get('member_id'))
        return request_get(url, kwargs)
