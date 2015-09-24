# -*- coding: utf-8 -*-
# author: cysnake4713
#
import unittest, json, copy
import tianvlib


@unittest.skip('skip attr')
class TianvSyncAttrTest(unittest.TestCase):
    def setUp(self):
        self.client = tianvlib.client
        init_product_value = {
            "id": 0,
            "Title": u"G209 美式弓形卸扣-测试",
            # "Seo_Description": None,
            # "Seo_Title": None,
            # "ParentId": 0,
            # "Base64_Picture": None,
            "Price": 0.0,
            # "Description": None,
            # "Detail": None,
            # "Base64_MultilinePicture": None,
            "TypeId": 1131,
            # "ProductType": u"实物产品",
            # "Obj_infoId": 9356,
            "Attribute_infos": [
                {
                    "AttributeName": u"属性",
                    "rule": u"单选",
                    "IsNum": u"服务",
                    "Type": u"默认类型",
                    "Parameter_Infos": [],
                }
            ],
            "Product_Number_Infos": []
        }
        result = self.client.AddProduct(product=json.dumps(init_product_value))
        self.assertTrue(result.get('R', False))
        self.product_id = int(result['Msg'])
        # print ('product_id = %s' % self.product_id)
        self.product_origin_value = self.client.GetProduct(id=self.product_id)
        # self.shuxin_id = self.product_origin_value['Attribute_infos'][0]['id']
        # print 'product_value = %s' % self.product_origin_value
        self.expect_attr_id = 0
        # print 'shuxin_id = %s' % self.shuxin_id

    def tearDown(self):
        self.client.delProduct(id=self.product_id)

    def clear_attr(self):
        target_value = []
        result = self.client.sync_product_param(product_id=self.product_id, json=json.dumps(target_value))
        self.assertTrue(result.get('R', False))

    def init_attr(self):
        self.clear_attr()
        origin_value = [
            {
                u'Min': 0,
                u'Max': 0,
                u'Product_Info_id': self.product_id,
                u'AttributeName': u"属性1",
                u'IsNum': u"服务",
                u"rule": u"单选",
                u'Parameter_Infos': [],
                u"Type": u"默认类型",
                u'id': 0
            },
            {
                u'Min': 0,
                u'Max': 0,
                u'Product_Info_id': self.product_id,
                u'AttributeName': u"属性2",
                u'IsNum': u"服务",
                u"rule": u"单选",
                u'Parameter_Infos': [],
                u"Type": u"默认类型",
                u'id': 0
            }]
        result = self.client.sync_product_param(product_id=self.product_id, json=json.dumps(origin_value))
        self.assertTrue(result.get('R', False))
        return self.client.GetProduct(id=self.product_id)['Attribute_infos']

    def get_result(self):
        return self.client.GetProduct(id=self.product_id)['Attribute_infos']

    @unittest.skip('skip create test')
    def test_sync_product_param_attribute_create(self):
        self.clear_attr()
        origin_value = [
            {
                u'Min': 0,
                u'Max': 0,
                u'Product_Info_id': self.product_id,
                u'AttributeName': u"属性1",
                u'IsNum': u"服务",
                u"rule": u"单选",
                u'Parameter_Infos': [],
                u"Type": u"默认类型",
                u'id': 0
            },
            {
                u'Min': 0,
                u'Max': 0,
                u'Product_Info_id': self.product_id,
                u'AttributeName': u"属性2",
                u'IsNum': u"服务",
                u"rule": u"单选",
                u'Parameter_Infos': [],
                u"Type": u"默认类型",
                u'id': 0
            }]
        # print 'origin_value =\t\t\t%s' % origin_value
        target_value = copy.deepcopy(origin_value)
        result = self.client.sync_product_param(product_id=self.product_id, json=json.dumps(origin_value))
        self.assertTrue(result.get('R', False))
        result = self.get_result()
        # print 'result =\t%s' % result
        target_value[0]['id'] = result[0]['id']
        target_value[1]['id'] = result[1]['id']

        self.assertEqual(result, target_value)

    def test_sync_product_param_attribute_modify(self):
        target_value = self.init_attr()
        target_value[0]['AttributeName'] = u"改变后属性值1"
        # print 'target_value= \t%s' % target_value
        result = self.client.sync_product_param(product_id=self.product_id, json=json.dumps(target_value))
        self.assertTrue(result.get('R', False))
        result = self.get_result()
        # print 'new_Attribute_infos =\t%s' % result
        self.assertEqual(result, target_value)

    def test_sync_product_param_attribute_modify_and_create(self):
        target_value = self.init_attr()
        target_value[0]['AttributeName'] = u"改变后属性值"
        target_value.append({
            u'Min': 0,
            u'Max': 0,
            u'Product_Info_id': self.product_id,
            u'AttributeName': u"新增属性",
            u'IsNum': u"服务",
            u"rule": u"单选",
            u'Parameter_Infos': [],
            u"Type": u"默认类型",
            u'id': 0,
        })
        result = self.client.sync_product_param(product_id=self.product_id, json=json.dumps(target_value))
        self.assertTrue(result.get('R', False))
        result = self.get_result()
        # print 'result =\t%s' % result
        target_value[2]['id'] = result[2]['id']
        self.assertEqual(result, target_value)

    def test_sync_product_param_attribute_modify_and_unlink(self):
        target_value = self.init_attr()
        target_value[0]['AttributeName'] = u"改变后属性值"
        del (target_value[1])
        result = self.client.sync_product_param(product_id=self.product_id, json=json.dumps(target_value))
        self.assertTrue(result.get('R', False))
        result = self.get_result()
        # print 'result =\t%s' % result
        self.assertEqual(result, target_value)

    def test_sync_product_param_attribute_create_modify_and_unlink(self):
        target_value = self.init_attr()
        target_value[0]['AttributeName'] = u"改变后属性值"
        del (target_value[1])
        target_value.append({
            u'Min': 0,
            u'Max': 0,
            u'Product_Info_id': self.product_id,
            u'AttributeName': u"新增属性",
            u'IsNum': u"服务",
            u"rule": u"单选",
            u'Parameter_Infos': [],
            u"Type": u"默认类型",
            u'id': 0,
        })
        result = self.client.sync_product_param(product_id=self.product_id, json=json.dumps(target_value))
        self.assertTrue(result.get('R', False))
        result = self.get_result()
        # print 'result =\t%s' % result
        target_value[1]['id'] = result[1]['id']
        self.assertEqual(result, target_value)


class TianvSyncParamTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.client = tianvlib.client
        init_product_value = {
            "id": 0,
            "Title": u"G209 美式弓形卸扣-测试",
            # "Seo_Description": None,
            # "Seo_Title": None,
            # "ParentId": 0,
            # "Base64_Picture": None,
            "Price": 0.0,
            # "Description": None,
            # "Detail": None,
            # "Base64_MultilinePicture": None,
            "TypeId": 1131,
            # "ProductType": u"实物产品",
            # "Obj_infoId": 9356,
            "Attribute_infos": [
                {
                    "AttributeName": u"属性",
                    "rule": u"单选",
                    "IsNum": u"服务",
                    "Type": u"默认类型",
                    "Parameter_Infos": [],
                }
            ],
            "Product_Number_Infos": []
        }
        result = self.client.AddProduct(product=json.dumps(init_product_value))
        self.assertTrue(result.get('R', False))
        self.product_id = int(result['Msg'])
        # print ('product_id = %s' % self.product_id)
        self.product_origin_value = self.client.GetProduct(id=self.product_id)
        # self.shuxin_id = self.product_origin_value['Attribute_infos'][0]['id']
        # print 'product_value = %s' % self.product_origin_value
        self.expect_attr_id = 0
        # print 'shuxin_id = %s' % self.shuxin_id

    def tearDown(self):
        self.client.delProduct(id=self.product_id)

    def clear_attr(self):
        target_value = []
        result = self.client.sync_product_param(product_id=self.product_id, json=json.dumps(target_value))
        self.assertTrue(result.get('R', False))

    def init_attr(self):
        self.clear_attr()
        origin_value = [
            {
                u'Min': 0,
                u'Max': 0,
                u'Product_Info_id': self.product_id,
                u'AttributeName': u"属性1",
                u'IsNum': u"服务",
                u"rule": u"单选",
                u'Parameter_Infos': [
                    {
                        u"id": 0,
                        u"odooId": None,
                        u"Att_Info_id": 0,
                        u"ParameterName": u"参数名1",
                        u"ImageFile": None,
                        u"colorValue": None,
                        u"TextValue": u"参数名1",
                        u"Coefficient": 0,
                        u"proId": self.product_id,
                        u"Remark": "",
                        u"Number": -1,
                        u"def": u"不选",
                    },
                    {
                        u"id": 0,
                        u"odooId": None,
                        u"Att_Info_id": 0,
                        u"ParameterName": u"参数名1",
                        u"ImageFile": None,
                        u"colorValue": None,
                        u"TextValue": u"参数名1",
                        u"Coefficient": 0,
                        u"proId": self.product_id,
                        u"Remark": "",
                        u"Number": -1,
                        u"def": u"不选",
                    },
                ],
                u"Type": u"默认类型",
                u'id': 0
            },
            {
                u'Min': 0,
                u'Max': 0,
                u'Product_Info_id': self.product_id,
                u'AttributeName': u"属性2",
                u'IsNum': u"服务",
                u"rule": u"单选",
                u'Parameter_Infos': [],
                u"Type": u"默认类型",
                u'id': 0
            }]
        result = self.client.sync_product_param(product_id=self.product_id, json=json.dumps(origin_value))
        self.assertTrue(result.get('R', False))
        return self.client.GetProduct(id=self.product_id)['Attribute_infos']

    def get_result(self):
        return self.client.GetProduct(id=self.product_id)['Attribute_infos']

    @unittest.skip('skip create')
    def test_param_create(self):
        self.clear_attr()
        origin_value = [
            {
                u'Min': 0,
                u'Max': 0,
                u'Product_Info_id': self.product_id,
                u'AttributeName': u"属性1",
                u'IsNum': u"服务",
                u"rule": u"单选",
                u'Parameter_Infos': [
                    {
                        u"id": 0,
                        u"odooId": None,
                        u"Att_Info_id": 0,
                        u"ParameterName": u"参数名1",
                        u"ImageFile": None,
                        u"colorValue": None,
                        u"TextValue": u"参数名1",
                        u"Coefficient": 0,
                        u"proId": self.product_id,
                        u"Remark": "",
                        u"Number": -1,
                        u"def": u"不选",
                    },
                    {
                        u"id": 0,
                        u"odooId": None,
                        u"Att_Info_id": 0,
                        u"ParameterName": u"参数名2",
                        u"ImageFile": None,
                        u"colorValue": None,
                        u"TextValue": u"参数名2",
                        u"Coefficient": 0,
                        u"proId": self.product_id,
                        u"Remark": "",
                        u"Number": -1,
                        u"def": u"不选",
                    },
                ],
                u"Type": u"默认类型",
                u'id': 0
            },
            {
                u'Min': 0,
                u'Max': 0,
                u'Product_Info_id': self.product_id,
                u'AttributeName': u"属性2",
                u'IsNum': u"服务",
                u"rule": u"单选",
                u'Parameter_Infos': [],
                u"Type": u"默认类型",
                u'id': 0
            }]
        # print 'origin_value =\t\t\t%s' % origin_value
        target_value = copy.deepcopy(origin_value)
        result = self.client.sync_product_param(product_id=self.product_id, json=json.dumps(origin_value))
        self.assertTrue(result.get('R', False))
        result = self.get_result()
        # print 'result =\t%s' % result
        target_value[0]['Parameter_Infos'][0]['id'] = result[0]['Parameter_Infos'][0]['id']
        target_value[0]['Parameter_Infos'][1]['id'] = result[0]['Parameter_Infos'][1]['id']
        target_value[0]['Parameter_Infos'][0]['Att_Info_id'] = result[0]['Parameter_Infos'][0]['Att_Info_id']
        target_value[0]['Parameter_Infos'][1]['Att_Info_id'] = result[0]['Parameter_Infos'][1]['Att_Info_id']

        target_value[0]['id'] = result[0]['id']
        target_value[1]['id'] = result[1]['id']

        self.assertEqual(result, target_value)

    def test_params_modify(self):
        target_value = self.init_attr()
        # print 'origin value\t%s' % json.dumps(target_value)
        target_value[0]['Parameter_Infos'][0]['ParameterName'] = u'新的参数名称'
        # print 'target value\t%s' % json.dumps(target_value)
        result = self.client.sync_product_param(product_id=self.product_id, json=json.dumps(target_value))
        self.assertTrue(result.get('R', False))
        result = self.get_result()
        # print 'result value\t%s' % json.dumps(result)
        self.assertEqual(result, target_value)

    def test_params_add(self):
        target_value = self.init_attr()
        print target_value
        target_value[0]['Parameter_Infos'].append({
            u"id": 0,
            u"odooId": None,
            u"Att_Info_id": 0,
            u"ParameterName": u"参数名3",
            u"ImageFile": None,
            u"colorValue": None,
            u"TextValue": u"参数名3",
            u"Coefficient": 0,
            u"proId": self.product_id,
            u"Remark": "",
            u"Number": -1,
            u"def": u"不选",
        })

        print target_value

        result = self.client.sync_product_param(product_id=self.product_id, json=json.dumps(target_value))
        self.assertTrue(result.get('R', False))
        result = self.get_result()
        print result
        self.assertTrue(len(result[0]['Parameter_Infos']) == 3)
        target_value[0]['Parameter_Infos'][2]['id'] = result[0]['Parameter_Infos'][2]['id']
        target_value[0]['Parameter_Infos'][2]['Att_Info_id'] = result[0]['Parameter_Infos'][2]['Att_Info_id']
        self.assertEqual(result, target_value)

    def test_params_delete(self):
        target_value = self.init_attr()
        del target_value[0]['Parameter_Infos'][0]
        result = self.client.sync_product_param(product_id=self.product_id, json=json.dumps(target_value))
        self.assertTrue(result.get('R', False))
        result = self.get_result()
        self.assertEqual(result, target_value)

if __name__ == '__main__':
    unittest.main()
