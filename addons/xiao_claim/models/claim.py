# -*- coding: utf-8 -*-
# author: cysnake4713
#

from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class Claim(models.Model):
    _name = 'xiao.claim'
    _rec_name = 'order_id'
    _description = 'Xiao Claim'

    state = fields.Selection([('processing', 'Processing'),
                              ('finished', 'Finished'),
                              # ('refund', 'Refund'),
                              # ('switched', 'Switched'),
                              ('rejected', 'Rejected'),
                              ('canceled', 'Canceled'),
                              ], 'State', default='processing')
    user_id = fields.Many2one('res.users', 'Related User')
    order_id = fields.Many2one('sale.order', 'Related Order', required=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', 'Partner', related='order_id.partner_id', readonly=True)

    carrier_id = fields.Char('Carrier')
    carrier_tracking_ref = fields.Char('Carrier Tracking Ref')
    description = fields.Text('Description')

    new_carrier_id = fields.Char('New Carrier')
    new_carrier_tracking_ref = fields.Char('New Carrier Tracking Ref')
    response_description = fields.Text('Response Description')

    returned_products = fields.Many2many('product.product', 'xiao_claim_product_rel', 'claim_id', 'product_id', 'Returned Product')
