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
        if 'id' in data:
            partner_id = data.pop('id')
            self.env['res.partner'].browse(partner_id).write(data)
        else:
            data['is_company'] = True
            data['']
            data['company_id'] = self.env['ir.config_parameter'].get_param('interface.partner_company_default')
            partner_id = self.env['res.partner'].create(data).id
        return partner_id
