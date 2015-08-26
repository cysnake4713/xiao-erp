# -*- coding: utf-8 -*-
# __author__ = cysnake4713@gmail.com
{
    'name': 'Xiao Wechat Auto Module',
    'version': '0.2',
    'category': 'odoosoft',
    'complexity': "easy",
    'description': """
Xiao Wechat Auto""",
    'author': 'Matt Cai',
    'website': 'http://odoosoft.com',
    'depends': ['base', 'base_action_rule', 'odoosoft_wechat_enterprise', 'sale'],
    'data': [
        'data/sale_order_wechat_data.xml',
        'data/sale_order_wechat_auto.xml',

        'data/stock_move_wechat_data.xml',
        'data/stock_move_wechat_auto.xml',

        'data/website_pay_wechat_data.xml',
        'data/website_pay_wechat_auto.xml',

        'data/xiao_claim_wechat_data.xml',
        'data/xiao_claim_wechat_auto.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    'application': True
}
