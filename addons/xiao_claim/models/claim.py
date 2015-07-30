# -*- coding: utf-8 -*-
# author: cysnake4713
#

from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class Claim(models.Model):
    _name = 'xiao.claim'
    _rec_name = 'order'
    _description = 'Xiao Claim'

    order = fields.Many2one('sale.order', 'Related Order', required=True)
    partner_id = fields.Many2one('res.partner', 'Partner', related='order.partner_id', readonly=True)
    state = fields.Selection([('processing', 'Processing'),
                              ('Returned', 'Returned'),
                              ('rejected', 'Rejected'),
                              ('canceled', 'Canceled'),
                              ], 'State', default='processing')
    description = fields.Text('Description')
    carrier_id = fields.Char('Carrier')
    carrier_tracking_ref = fields.Char('Carrier Tracking Ref')
