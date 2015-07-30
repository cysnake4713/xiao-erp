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

    state = fields.Selection([('processing', 'Processing'),
                              ('finished', 'Finished'),
                              # ('refund', 'Refund'),
                              # ('switched', 'Switched'),
                              ('rejected', 'Rejected'),
                              ('canceled', 'Canceled'),
                              ], 'State', default='processing')
    user_id = fields.Many2one('res.users', 'Related User')
    order = fields.Many2one('sale.order', 'Related Order', required=True)
    partner_id = fields.Many2one('res.partner', 'Partner', related='order.partner_id', readonly=True)

    carrier_id = fields.Char('Carrier')
    carrier_tracking_ref = fields.Char('Carrier Tracking Ref')
    description = fields.Text('Description')

    new_carrier_id = fields.Char('New Carrier')
    new_carrier_tracking_ref = fields.Char('New Carrier Tracking Ref')
    response_description = fields.Text('Response Description')
