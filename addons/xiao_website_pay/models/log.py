# -*- coding: utf-8 -*-
# author: cysnake4713
#
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class WebsitePayLog(models.Model):
    _name = 'xiao.website.pay.log'
    _rec_name = 'tianv_id'
    _description = 'Xiao Website Pay Log'
    _order = 'id desc'

    tianv_id = fields.Char('Tianv ID', required=True)
    related_order_ids = fields.Many2many('sale.order', 'tianv_pay_order_rel', 'log_id', 'order_id', 'Related Orders')
    closed_order_ids = fields.Many2many('sale.order', 'tianv_pay_close_order_rel', 'log_id', 'order_id', 'Closed Orders')
    price = fields.Float('Price', digits=(10, 2))
    pay_datetime = fields.Datetime('Pay Datetime')
    is_reconciled = fields.Boolean('Is Reconciled')
