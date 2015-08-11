# -*- coding: utf-8 -*-
# author: cysnake4713
#

from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp


class CashBackRecord(models.Model):
    _name = 'xiao.cash.back.record'
    _rec_name = 'name'
    _description = 'Cash Back Record'

    name = fields.Char('Cash Back Name', required=True)
    period_from = fields.Many2one('account.period', 'Period From', required=True)
    period_to = fields.Many2one('account.period', 'Period To', required=True)
    config_id = fields.Many2one('xiao.cash.back.config', 'Used Config', required=True)
    is_closed = fields.Boolean('Is Closed')

    line_ids = fields.One2many('xiao.cash.back.line', 'record_id', 'Cash Back Lines')

    @api.multi
    def button_generate_all_record(self):
        self.line_ids.unlink()
        need_compute_partners = self.env['res.partner'].search([('customer', '=', True)])
        for custom in need_compute_partners:
            self.line_ids.create({'record_id': self.id, 'partner_id': custom.id})
        self.button_regenerate_cash_back_value()
        return True

    @api.multi
    def button_regenerate_cash_back_value(self):
        # self.env.cr.execute("""
        #     SELECT l.partner_id, sum(l.debit) as debit, sum(l.credit) as credit
        #     FROM account_move_line as l
        #     WHERE  l.date >=%s and l.date <= %s and l.account_id in %s
        #     GROUP BY partner_id
        #     """, [self.period_from.date_start, self.period_to.date_stop, tuple([a.id for a in self.config_id.account_ids])])
        self.env.cr.execute("""
            SELECT l.partner_id, sum(l.amount) as amount
            FROM account_voucher as l
            WHERE  l.date >=%s and l.date <= %s and l.type = 'receipt'
            GROUP BY partner_id
            """, [self.period_from.date_start, self.period_to.date_stop])
        paid_maps = {v[0]: v[1] for v in self.env.cr.fetchall()}
        for line in self.line_ids:
            if line.partner_id.id in paid_maps:
                total_paid = paid_maps[line.partner_id.id]
                will_cash_back = self.config_id.get_cash_back(total_paid)
                line.total_paid = total_paid
                line.will_cash_back = will_cash_back
            else:
                line.total_paid = 0.0
                line.will_cash_back = 0.0

        return True


class CashBackLine(models.Model):
    _name = 'xiao.cash.back.line'
    _rec_name = 'partner_id'
    _description = 'Cash Back Line'

    record_id = fields.Many2one('xiao.cash.back.record', 'Related Record', ondelete='cascade')

    partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    total_paid = fields.Float('Total Paid', digits=dp.get_precision('Account'))
    will_cash_back = fields.Float('Will Cash Back', digits=dp.get_precision('Account'))
    is_cash_back = fields.Boolean('Is Cash Backed')
    cash_back_bank = fields.Many2one('res.partner.bank')
    cash_back_date = fields.Date('Cash Back Date')


class CashBackConfig(models.Model):
    _name = 'xiao.cash.back.config'
    _rec_name = 'name'
    _description = 'Cash Back Config'

    name = fields.Char('Name', required=True)
    cash_back_rate = fields.Float('Cash Back Rate')
    account_ids = fields.Many2many('account.account', 'cash_back_config_account_rel', 'config_id', 'account_id', 'Need compute Accounts',
                                   domain=[('type', '!=', 'view')])

    @api.multi
    def get_cash_back(self, total_value):
        return self.cash_back_rate * total_value
