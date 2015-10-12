# -*- coding: utf-8 -*-
# __author__ = cysnake4713@gmail.com
{
    'name': 'Xiao Expense Module',
    'version': '0.2',
    'category': 'xiao_expense',
    'complexity': "easy",
    'description': """
Xiao Expense""",
    'author': 'Matt Cai',
    'website': 'http://odoosoft.com',
    'depends': ['base', 'account', 'odoosoft_workflow'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'data/data.xml',

        'views/menuitem.xml',
        'views/expense_view.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    'application': True
}
