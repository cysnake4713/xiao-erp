# -*- coding: utf-8 -*-
# author: cysnake4713
#

from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class PartnerConfig(models.TransientModel):
    _name = 'interface.config.settings'
    _inherit = 'res.config.settings'

    # product
    product_type_default = fields.Char('Tianv Product Type default')
    # partner
    partner_company_default = fields.Many2one('res.company', 'Partner Company Default')

    _defaults = {
        'partner_company_default': lambda self, cr, uid, ct:
            self.pool['ir.config_parameter'].get_param(cr, uid, 'interface.partner_company_default',
                                                       ct),
        'product_type_default': lambda self, cr, uid, ct: int(
            self.pool['ir.config_parameter'].get_param(cr, uid, 'tianv.product.type',
                                                       ct)),
    }

    @api.multi
    def set_default_info(self):
        self.env['ir.config_parameter'].set_param('tianv.product.type', self.product_type_default)
        self.env['ir.config_parameter'].set_param('interface.partner_company_default', str(self.partner_company_default.id))

        # @api.multi
        # def button_backup_db(self):
        #     return self.env['interface.config.settings'].cron_backup_db()
