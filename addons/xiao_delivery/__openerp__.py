# -*- coding: utf-8 -*-
# __author__ = cysnake4713@gmail.com
{
    'name': 'Xiao Delivery Module',
    'version': '0.2',
    'category': 'xiao',
    'complexity': "easy",
    'description': """
Xiao Delivery""",
    'author': 'Matt Cai',
    'website': 'http://odoosoft.com',
    'depends': ['base', 'delivery'],
    'data': [
        'views/delivery_view.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    'application': True
}
