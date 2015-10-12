# -*- coding: utf-8 -*-
# author: cysnake4713
#

from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class XiaoExpense(models.Model):
    _name = 'xiao.expense'
    _rec_name = 'name'
    _inherit = 'odoosoft.workflow.abstract'
    _description = 'Xiao Expense'

    name = fields.Char('Name', required=True)
    expense_date = fields.Date('Expense Date', default=fields.Date.today())
    user_id = fields.Many2one('res.users', 'User', default=lambda self: self.env.user)
    state = fields.Selection([('draft', 'Draft'), ('processing', 'Processing'), ('paid', 'Paid')], 'State', default='draft',
                             track_visibility='onchange')

    total = fields.Float('Total Price', digits=(10, 2), compute='_compute_total')

    line_ids = fields.One2many('xiao.expense.line', 'expense_id', 'Lines')

    @api.multi
    @api.depends('line_ids')
    def _compute_total(self):
        for expense in self:
            expense.total = sum([l.price for l in expense.line_ids])


class XiaoExpenseLine(models.Model):
    _name = 'xiao.expense.line'
    _rec_name = 'name'
    _description = 'Xiao Expense Line'

    name = fields.Char('Name', required=True)
    price = fields.Float('Price', digits=(10, 2))
    expense_id = fields.Many2one('xiao.expense', 'Expense', ondelete='cascade')
