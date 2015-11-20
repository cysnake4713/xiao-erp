# -*- coding: utf-8 -*-
# author: cysnake4713
#

from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _
from ..tianvlib import partner_client as client


class ResPartner(models.Model):
    _inherit = 'res.partner'

    tianv_id = fields.Integer('Tianv ID')
    tianv_last_update = fields.Char('Tianv Last Update')
    industry = fields.Char('Industry')
    company_type = fields.Char('Company Type')

    @api.model
    def sync_tianv_data(self):
        companys = self.search_read([('is_company', '=', True), ('tianv_id', '!=', 0)], ['tianv_id', 'tianv_last_update'])
        company_maps = {c['tianv_id']: (c['id'], c['tianv_last_update']) for c in companys}
        users = self.search_read([('is_company', '=', False), ('tianv_id', '!=', 0)], ['tianv_id', 'tianv_last_update'])
        user_maps = {c['tianv_id']: (c['id'], c['tianv_last_update']) for c in users}

        remote_result = client.GetPartnerIds()
        # sync company
        for remote_company in remote_result['company']:
            # new
            if remote_company['id'] not in company_maps:
                company_info = client.GetCompanyInfo(id=remote_company['id'])
                new_company = self.create({
                    'name': company_info['name'],
                    'tianv_id': company_info['id'],
                    'industry': company_info['industry'],
                    'company_type': company_info['companyType'],
                    'tianv_last_update': remote_company['lastUpdate'],
                    'is_company': True,
                    'company_id': self.env['ir.config_parameter'].get_param('interface.partner.company.default')
                })
                company_maps.update({remote_company['id']: (new_company.id, remote_company['lastUpdate'])})
            # update
            elif remote_company['lastUpdate'] != company_maps[remote_company['id']][1]:
                company_info = client.GetCompanyInfo(id=remote_company['id'])
                update_company = self.browse(company_maps[remote_company['id']][0]).write({
                    'name': company_info['name'],
                    'tianv_id': company_info['id'],
                    'industry': company_info['industry'],
                    'company_type': company_info['companyType'],
                    'tianv_last_update': remote_company['lastUpdate'],
                })

        # sync user
        for remote_user in remote_result['users']:
            # new
            if remote_user['id'] not in user_maps:
                user_info = client.GetUserInfo(id=remote_user['id'])
                new_user = self.create({
                    'name': user_info['name'],
                    'tianv_id': user_info['id'],
                    'tianv_last_update': remote_user['lastUpdate'],
                    'zip': user_info['zip'],
                    'street': user_info['address'],
                    'email': user_info['mail'],
                    'parent_id': company_maps[user_info['companyId']][0] if user_info['companyId'] in company_maps else 0,
                    'is_company': False,
                    'company_id': self.env['ir.config_parameter'].get_param('interface.partner.company.default')
                })
            # update
            elif remote_user['lastUpdate'] != user_maps[remote_user['id']][1]:
                user_info = client.GetUserInfo(id=remote_user['id'])
                update_user = self.browse(user_maps[remote_user['id']][0]).write({
                    'name': user_info['name'],
                    'tianv_id': user_info['id'],
                    'tianv_last_update': remote_user['lastUpdate'],
                    'zip': user_info['zip'],
                    'street': user_info['address'],
                    'email': user_info['mail'],
                    'parent_id': company_maps[user_info['companyId']][0] if user_info['companyId'] in company_maps else 0,
                })

    @api.model
    def cron_sync(self):
        self.sync_tianv_data()
