# coding=utf-8
__author__ = 'cysnak4713'

import json
from suds.client import Client
from openerp.tools import config
from openerp import exceptions


class OAProductClient:
    # def __init__(self):
    #     self.HASH_CODE = config.get('oa_hass_code')

    def __init__(self):
        pass

    def __getattr__(self, attr):
        # if config.get('oa_is_sync'):
        #     # if False:
        return _ProductExecutable(attr)
        # else:
        #     return lambda **o: None


class _ProductExecutable(object):
    def __init__(self, method):
        self.HTTP = 'http://%s/plugins/Tianv_Mall_WS/MallProductWS.asmx?wsdl' % config.get('tianv_server', 'test.tianv.net')
        self.method = method

    def __call__(self, **kw):
        oa_client = Client(self.HTTP).service
        function = getattr(oa_client, self.method)
        if 'key' not in kw:
            kw['username'] = config.get('tianv_name', 'admin')
            kw['pwd'] = config.get('tianv_pwd', '123456')
        result = function(**kw)
        result = json.loads(result)
        if not result.get('R', True):
            raise exceptions.Warning(u'同步远程服务器出错:%s' % result.get('Msg', result))
        return result

    def __str__(self):
        return '_Executable (%s %s)' % (self._method, self._path)

    __repr__ = __str__


class OAPartnerClient:
    # def __init__(self):
    #     self.HASH_CODE = config.get('oa_hass_code')

    def __init__(self):
        pass

    def __getattr__(self, attr):
        # if config.get('oa_is_sync'):
        #     # if False:
        return _PartnerExecutable(attr)
        # else:
        #     return lambda **o: None


class _PartnerExecutable(object):
    def __init__(self, method):
        self.HTTP = 'http://%s/plugins/Tianv_Mall_WS/MallPartnerWS.asmx?wsdl' % config.get('tianv_server', 'test.tianv.net')
        self.method = method

    def __call__(self, **kw):
        oa_client = Client(self.HTTP).service
        function = getattr(oa_client, self.method)
        kw['key'] = config.get('tianv_key', '1DE19422-0D6D-49C8-B17C-59542CE73A3A')
        result = function(**kw)
        result = json.loads(result)
        if not result.get('R', True):
            raise exceptions.Warning(u'同步远程服务器出错:%s' % result.get('Msg', result))
        return result

    def __str__(self):
        return '_Executable (%s %s)' % (self._method, self._path)

    __repr__ = __str__


product_client = OAProductClient()
partner_client = OAPartnerClient()

if __name__ == '__main__':
    # json_params = (
    # {"msgid": 1122231, "class_code": 144, "title": u"文章标题", "author": u"张小虎", "deptname": u"信息发布中心", "deptcode": 78, "content": u"文章内容",
    #      "readcount": 122,
    #      "createdate": "2001-01-01T00:00:00", "overduedate": "2001-02-01T00:00:00", "lastmodidate": "2001-01-01T00:00:00"}
    # )

    local_client = Client('http://test.tianv.net/plugins/Tianv_Mall_WS/MallProductWS.asmx?wsdl')

    # local_client.service.DelProduct_Number(id=1, username='admin', pwd='123456')
    print local_client.service.GetProduct(id=34, username='admin', pwd='123456')
    # local_client.service.AddOrEditProduct_Number_Info(proid=34, Product_Number_InfoJson=json.dumps([
    #     {"id": 0,
    #      "Product_Info_id": 29,
    #      "parIds": '83',
    #      "parNames": "undefined",
    #      "Number": 1,
    #      "Price": 1,
    #      }
    # ]), username='admin', pwd='123456')
    # temp_value = [{
    #     "id": 22,
    #     "Product_Info_id": 18,
    #     "AttributeName": "111测试sw",
    #     "rule": u"单选",
    #     "Max": 0,
    #     "Min": 0,
    #     "IsNum": u"服务",
    #     "Type": u"默认类型",
    #     "Parameter_Infos": []
    # }]
    # print local_client.service.sync_product_param(product_id=18,
    #                                               json=json.dumps(temp_value),  # json=json.dumps(product_value),
    #                                               username='admin', pwd='123456')
    # print local_client
    # product_value = {
    #     "Title": "asdf",
    #     "Seo_Description": "",
    #     "Seo_Title": "sss",
    #     "ProductType": "ssss",
    #     "Price": 10,
    #     "TypeId": 1131,
    # }
    # json.dumps(product_value)
    # print local_client.service.AddProduct(product=json.dumps(product_value), username='admin', pwd='123456')
