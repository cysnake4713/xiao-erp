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
        sock_common = xmlrpclib.ServerProxy('http://' + OPENERP_URL + '/xmlrpc/common')
        self.uid = sock_common.login(self.dbname, username, self.pwd)
        self.client = xmlrpclib.ServerProxy('http://' + OPENERP_URL + '/xmlrpc/object')

    def test_partner_sync(self):
        data = {
            'name': 'test',
        }
        self.client.execute(self.dbname, self.uid, self.pwd, 'interface.interface', 'interface_sync_user', data)
