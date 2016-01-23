# -*- coding: utf-8 -*-
# author: cysnake4713
#

from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class InterfaceWizard(models.AbstractModel):
    _name = 'interface.interface'

    @api.model
    def interface_sync_user(self, data):
        # pre process country and state
        if 'country_id' in data:
            country_id = self.env['res.country'].search([('code', '=', data['country_id'])])
            data['country_id'] = country_id[0].id if country_id else False
        if 'state_id' in data:
            state_id = self.env['res.country.state'].search([('name', 'like', '%%%s%%' % data['state_id'])])
            data['state_id'] = state_id[0].id if state_id else False

        if 'id' in data:
            partner_id = data.pop('id')
            self.env['res.partner'].browse(partner_id).write(data)
        else:
            data['is_company'] = True
            data['company_id'] = self.env['ir.config_parameter'].get_param('interface.partner_company_default')
            partner_id = self.env['res.partner'].create(data).id
        return partner_id


class SyncLog(models.Model):
    _name = 'interface.sync.log'
    _rec_name = 'name'
    _description = 'Sync Log'
    _order = 'log_datetime desc'

    log_datetime = fields.Datetime('Log Datetime', default=lambda obj: fields.Datetime.now())
    model = fields.Char('Model')
    type = fields.Char('Status')
    name = fields.Char('Info')

    @api.model
    def info(self, model, name):
        self.create({
            'model': model,
            'type': 'info',
            'name': name,
        })

    @api.model
    def error(self, model, name):
        self.create({
            'model': model,
            'type': 'error',
            'name': name,
        })
