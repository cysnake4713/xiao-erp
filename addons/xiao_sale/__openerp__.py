# -*- coding: utf-8 -*-
# __author__ = cysnake4713@gmail.com
{
    'name': 'Xiao Sale Update Module',
    'version': '0.2',
    'category': 'odoosoft',
    'complexity': "easy",
    'description': """
Xiao Sale Update Module""",
    'author': 'Matt Cai',
    'website': 'http://odoosoft.com',
    'depends': ['base', 'sale', 'purchase'],
    'data': [
        # 'security/ir.model.access.csv',

        # 'views/product_template_view.xml',
        # 'views/limit_level_view.xml',
        'views/purchase_view.xml',
        'views/partner_view.xml',
        # 'views/partner_wizard.xml',
        # 'views/menuitem.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    'application': True
}
