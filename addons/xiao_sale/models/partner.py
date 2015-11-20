# -*- coding: utf-8 -*-
# author: cysnake4713
#

from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp


class ResPartner(models.Model):
    _inherit = 'res.partner'

    qq = fields.Char('QQ')

    tianv_id = fields.Char('Tianv ID')