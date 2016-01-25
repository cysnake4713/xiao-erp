# -*- coding: utf-8 -*-
# __author__ = cysnake4713@gmail.com
{
    'name': 'Xiao Interface Module',
    'version': '0.2',
    'category': 'odoosoft',
    'complexity': "easy",
    'description': """
Xiao Interface""",
    'author': 'Matt Cai',
    'website': 'http://odoosoft.com',
    'depends': ['base', 'product', 'sale', 'xiao_website_pay', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_view.xml',
        'views/sale_view.xml',
        'views/menu.xml',
        'views/tianv_product_map.xml',
        'views/product_view.xml',
        'views/partner_view.xml',
        'views/base_setup_view.xml',
        'data/cron.xml',
        'data/param.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    'application': True
}
