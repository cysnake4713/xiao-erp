# -*- coding: utf-8 -*-
# author: cysnake4713
#

from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp


class InvoiceInherit(models.Model):
    _inherit = 'account.invoice'

    invoice_company_name = fields.Char('Invoice Company Name')
    real_invoice_ids = fields.One2many('account.invoice.real.line', 'invoice_id', 'Real Invoices')


class RealInvoice(models.Model):
    _name = 'account.invoice.real.line'
    _rec_name = 'real_invoice_number'
    _order = 'real_invoice_date desc'
    _description = 'Account Invoice Real Line'

    invoice_id = fields.Many2one('account.invoice', 'Related Invoice', ondelete='cascade')

    real_invoice_number = fields.Char('Real Invoice Number')
    real_invoice_date = fields.Date('Real Invoice Date', default=lambda self: fields.Date.today())
    real_invoice_amount = fields.Float('Real Invoice Amount', digits=dp.get_precision('Account'))
    comment = fields.Char('Comment')
