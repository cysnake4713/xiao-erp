# -*- coding: utf-8 -*-
# author: cysnake4713
#
from openerp import tools, exceptions
from openerp import models, fields, api
from openerp.tools.translate import _


class PartnerWizard(models.TransientModel):
    _name = 'res.partner.wizard.login'
    _rec_name = 'login'

    partner = fields.Many2one('res.partner', 'Related Partner')
    login = fields.Char('Login Name', required=True)
    password = fields.Char('Login Password', required=True)
    password_confirm = fields.Char('Login Password Confirm', required=True)

    @api.model
    def default_get(self, fields_list):
        result = super(PartnerWizard, self).default_get(fields_list)
        partner = self.env['res.partner'].browse(self.env.context['active_id'])
        result['partner'] = partner.id
        result['login'] = partner.login_name
        return result

    @api.multi
    def button_change_login(self):
        if self.password != self.password_confirm:
            raise exceptions.Warning(_('Two Password Not Match'))
        else:
            self.partner.login_name = self.login
            self.partner.login_password = self.password
            return True
