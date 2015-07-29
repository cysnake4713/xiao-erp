# -*- coding: utf-8 -*-
# author: cysnake4713
#

from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class ReturnGood(models.Model):
    _name = 'xiao.return.good'
    _rec_name = 'order'
    _description = 'Xiao Return Goods'

    order = fields.Many2one('sale.order', 'Related Order', required=True)
    state = fields.Selection([('processing', 'Processing'),
                              ('confirmed', 'Confirmed'),
                              ('Returned', 'Returned'),
                              ('rejected', 'Rejected'),
                              ('canceled', 'Canceled'),
                              ], 'State')
    description = fields.Text('Description')
