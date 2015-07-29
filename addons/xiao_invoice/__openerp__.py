# -*- coding: utf-8 -*-
# __author__ = cysnake4713@gmail.com
{
    'name': 'Xiao Invoice Update Module',
    'version': '0.2',
    'category': 'odoosoft',
    'complexity': "easy",
    'description': """
Xiao Invoice Update""",
    'author': 'Matt Cai',
    'website': 'http://odoosoft.com',
    'depends': ['base', 'sale', 'account'],
    'data': [
        'views/order_view.xml',
        'views/invoice_view.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    'application': True
}
