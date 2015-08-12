# -*- coding: utf-8 -*-
# __author__ = cysnake4713@gmail.com
{
    'name': 'Xiao Claim Module',
    'version': '0.2',
    'category': 'odoosoft',
    'complexity': "easy",
    'description': """
Xiao Claim""",
    'author': 'Matt Cai',
    'website': 'http://odoosoft.com',
    'depends': ['base', 'sale', 'product'],
    'data': [
        'security/ir.model.access.csv',

        'views/menuitem.xml',
        'views/claim_view.xml',
        'views/order_view.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    'application': True
}
