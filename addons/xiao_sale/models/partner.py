# -*- coding: utf-8 -*-
# author: cysnake4713
#

from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp


class LimitLevel(models.Model):
    _name = 'xiao.partner.limit.level'
    _rec_name = 'name'
    _description = 'Xiao Partner Limit Level'

    name = fields.Char('Name', required=True)
    value = fields.Float('Max Value', digits=(10, 2))
    is_default = fields.Boolean('Is Default')

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, u'%s (%s)' % (record.name, record.value)))
        return result


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _default_sale_limit(self):
        default_value = self.env['xiao.partner.limit.level'].search([('is_default', '=', True)])
        if default_value:
            return default_value[0]
        else:
            return self.env['xiao.partner.limit.level']

    qq = fields.Char('QQ')
    sale_limit = fields.Many2one('xiao.partner.limit.level', 'Sale Limit', default=_default_sale_limit)
    credit_left = fields.Float('Credit Left', digits=dp.get_precision('Account'), compute='_compute_credit_count')
    # override default
    # credit_limit = fields.Float('Credit Limit', digits=dp.get_precision('Account'), compute='_compute_credit_count')

    business_lesson = fields.File('Business Lesson')
    state = fields.Selection([('draft', 'Draft'), ('validated', 'Validated'), ('locked', 'Locked')], 'State', default='draft')

    tianv_id = fields.Char('Tianv ID')

    _sql_constraints = [('partner_login_name_unique', 'unique(login_name)', _('Login Name must be unique !'))]

    @api.multi
    def _compute_credit_count(self):
        for partner in self:
            if partner.sale_limit:
                partner.credit_left = partner.sale_limit.value - partner.credit
                # partner.credit_limit = partner.sale_limit.value
            else:
                partner.credit_left = 0.0
                # partner.credit_limit = 0.0

    @api.multi
    def button_credit_left_list(self):
        res = self.env['ir.actions.act_window'].for_xml_id('account', 'action_invoice_refund_out_tree')
        res['domain'] = [('type', 'in', ['out_invoice', 'out_refund']), ('state', 'not in', ['draft', 'cancel', 'paid']),
                         ('partner_id', '=', self.id)]
        return res

    @api.multi
    def button_validated_partner(self):
        for partner in self:
            partner.state = 'validated'

    @api.multi
    def button_locked_partner(self):
        for partner in self:
            partner.state = 'locked'
