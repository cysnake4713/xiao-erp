# -*- coding: utf-8 -*-
# author: cysnake4713
#

from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _
from ..tianvlib import product_client as client


class ResPartner(models.Model):
    _inherit = 'res.partner'

    tianv_id = fields.Integer('Tianv ID')
    industry = fields.Char('Industry')
    company_type = fields.Char('Company Type')

    @api.model
    def sync_tianv_data(self):

        last_update = self.env['ir.config_parameter'].get_param('interface.partner.last.update', 'False')
        if last_update == 'False':
            remote_result = client.GetUserIds()
        else:
            remote_result = client.GetOrderIds(updateTime=last_update)

        # sync company
        for remote_company_id in remote_result['company']:
            company_id = self.search([('tianv_id', '=', remote_company_id)])
            company_info = client.GetCompanyInfo(id=remote_company_id)
            # new
            if not company_id:
                new_company = self.create({
                    'name': company_info['name'],
                    'tianv_id': company_info['id'],
                    'industry': company_info['industry'],
                    'company_type': company_info['companyType'],
                    'is_company': True,
                    'company_id': eval(self.env['ir.config_parameter'].get_param('interface.partner.company.default', 'False'))
                })
            # update
            else:
                company_id.write({
                    'name': company_info['name'],
                    'tianv_id': company_info['id'],
                    'industry': company_info['industry'],
                    'company_type': company_info['companyType'],
                })

        # sync user
        for remote_user_id in remote_result['users']:
            user_id = self.search([('is_company', '=', False), ('tianv_id', '=', remote_user_id)])
            user_info = client.GetUserInfo(id=remote_user_id)
            if user_info['companyId']:
                parent_id = self.search([('is_company', '=', True), ('tianv_id', '=', user_info['companyId'])])
                if parent_id:
                    parent_id = parent_id[0].id
            else:
                parent_id = False

            # new
            if not user_id:
                new_user = self.create({
                    'name': user_info['name'],
                    'tianv_id': user_info['id'],
                    'zip': user_info['zip'],
                    'street': user_info['address'],
                    'email': user_info['mail'],
                    'parent_id': parent_id,
                    'is_company': False,
                    'company_id': eval(self.env['ir.config_parameter'].get_param('interface.partner.company.default', 'False'))
                })
            # update
            else:
                user_id.write({
                    'name': user_info['name'],
                    'tianv_id': user_info['id'],
                    'zip': user_info['zip'],
                    'street': user_info['address'],
                    'email': user_info['mail'],
                    'parent_id': parent_id,
                })
        self.env['ir.config_parameter'].set_param('interface.partner.last.update', fields.Datetime.now())

    @api.multi
    def button_sync_now(self):
        self.sync_tianv_data()

    @api.model
    def cron_sync(self):
        try:
            self.env.cr.execute('SAVEPOINT sync_partners')
            self.sync_tianv_data()
        except Exception, e:
            self.env['interface.sync.log'].create({'name': str(e)})
            self.env.cr.execute('ROLLBACK TO SAVEPOINT sync_partners')
        self.env.cr.execute('RELEASE SAVEPOINT sync_partners')
        return True
