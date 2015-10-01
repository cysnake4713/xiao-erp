# -*- coding: utf-8 -*-
# __author__ = cysnake4713@gmail.com
{
    'name': 'Xiao Product Module',
    'version': '0.2',
    'category': 'xiao',
    'complexity': "easy",
    'description': """
Xiao Product""",
    'author': 'Matt Cai',
    'website': 'http://odoosoft.com',
    'depends': ['base', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_view.xml',
        'data/param.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
}
