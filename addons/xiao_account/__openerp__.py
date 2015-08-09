# -*- coding: utf-8 -*-
# __author__ = cysnake4713@gmail.com
{
    'name': 'Xiao Xiao Account Update Module',
    'version': '0.2',
    'category': 'xiaoxiao',
    'complexity': "easy",
    'description': """
Xiao Xiao Account Update""",
    'author': 'Matt Cai',
    'website': 'http://odoosoft.com',
    'depends': ['base', 'account', 'account_cancel', 'oecn_account_print', 'odoosoft_account', 'account_renumber'],
    'data': [
        'views/renumber_view.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    'application': True
}
