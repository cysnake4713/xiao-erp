# coding=utf-8
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    delivery_address = fields.Char('Delivery Address')
    delivery_name = fields.Char('Delivery Name')
    delivery_phone = fields.Char('Delivery Phone')
    deliveryPrice = fields.Float('Delivery Price')
