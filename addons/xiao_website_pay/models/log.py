# -*- coding: utf-8 -*-
# author: cysnake4713
#
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class WebsitePayLog(models.Model):
    _name = 'xiao.website.pay.log'
    _rec_name = 'name'
    _description = 'Xiao Website Pay Log'

    name = fields.Char('Pay Description')
    order_id = fields.Many2one('sale.order', 'Order')
    price = fields.Float('Price', digits=(10, 2))
    pay_datetime = fields.Datetime('Pay Datetime')
