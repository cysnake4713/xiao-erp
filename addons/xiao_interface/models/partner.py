# -*- coding: utf-8 -*-
# author: cysnake4713
#

from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    tianv_id = fields.Char('Tianv ID')
    tianv_last_update = fields.Char('Tianv Last Update')
