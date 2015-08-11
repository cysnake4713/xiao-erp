# -*- coding: utf-8 -*-
# __author__ = cysnake4713@gmail.com
{
    'name': 'Xiao Cash back Module',
    'version': '0.2',
    'category': 'xiao',
    'complexity': "easy",
    'description': """
Xiao Cash back""",
    'author': 'Matt Cai',
    'website': 'http://odoosoft.com',
    'depends': ['base', 'account'],
    'data': [
        'views/menuitem.xml',
        'views/record_view.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    'application': True
}
