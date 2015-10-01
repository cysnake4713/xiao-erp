# -*- coding: utf-8 -*-
# author: cysnake4713
#
import unittest
import xmlrpclib


class TestPartner(unittest.TestCase):
    def setUp(self):
        username = 'admin'  # the user
        self.pwd = 'xiao_2015'  # the password of the user
        self.dbname = 'xiao-erp'  # the database
        OPENERP_URL = 'localhost:8069'

        # username = 'admin'  # the user
        # self.pwd = 'xiao_2015'  # the password of the user
        # self.dbname = 'xiao-test'  # the database
        # OPENERP_URL = 'toa.szstc.co'
        sock_common = xmlrpclib.ServerProxy('http://' + OPENERP_URL + '/xmlrpc/common')
        self.uid = sock_common.login(self.dbname, username, self.pwd)
        self.client = xmlrpclib.ServerProxy('http://' + OPENERP_URL + '/xmlrpc/object')

    def test_partner_sync(self):
        file = open('/home/cysnake4713/Pictures/选区_014.png', 'rb').read().encode('base64')
        data = {
            'name': '客户公司名称',
            'email': 'aa@163.com',  # Email
            'mobile': '1234124',  # Mobile
            'country_id': 'CN',  # Address_Country 中国就是CN, 其它国家的暂时不传递都行呢
            'state_id': '江苏',  # Address_Province
            'city': '盐城',  # Address_City
            'street': '九龙山东街22号地下',  # Address_Street
            'street2': '辅助地址',  # Address_Contact
            'zip': '208343',  # Address_Zip
            'phone': '15845645',  # Address_Tel1
            'fax': '1549542',  # Address_Tel2
            'qq': '54681354',  # Contact_QQ
            'business_lesson': file,  # 营业执照 base64处理
            'tianv_id': '1123',  # tianv相关id

        }
        self.client.execute(self.dbname, self.uid, self.pwd, 'interface.interface', 'interface_sync_user', data)
