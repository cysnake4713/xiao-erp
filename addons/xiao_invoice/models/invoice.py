# -*- coding: utf-8 -*-
# author: cysnake4713
#

from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class InvoiceInherit(models.Model):
    _inherit = 'account.invoice'

    invoice_company_name = fields.Char('Invoice Company Name')

