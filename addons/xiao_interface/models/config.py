# -*- coding: utf-8 -*-
# author: cysnake4713
#

from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _


class PartnerConfig(models.TransientModel):
    _name = 'interface.config.settings'
    _inherit = 'res.config.settings'

    # product type
    product_type_default = fields.Char('Tianv Product Type default')
    # product type parent
    product_type_parent_default = fields.Char('Tianv Product Parent Type default')
    # partner
    partner_company_default = fields.Many2one('res.company', 'Partner Company Default')

    partner_warehouse_default = fields.Many2one('stock.warehouse', 'Warehouse Default')

    order_tax_default = fields.Many2one('account.tax', 'Order Account Tax')

    order_delivery_default = fields.Many2one('product.product', 'Delivery Product')
    # order sale man
    order_user_default = fields.Many2one('res.users', 'Order Default User')

    delivery_company_code = fields.Char('Delivery Company Code')

    _defaults = {
        'partner_company_default': lambda self, cr, uid, ct: eval(
            self.pool['ir.config_parameter'].get_param(cr, uid, 'interface.partner.company.default', 'False', ct)),
        'partner_warehouse_default': lambda self, cr, uid, ct: eval(
            self.pool['ir.config_parameter'].get_param(cr, uid, 'interface.warehouse.company.default', 'False', ct)),
        'product_type_default': lambda self, cr, uid, ct: eval(
            self.pool['ir.config_parameter'].get_param(cr, uid, 'tianv.product.type', 'False', ct)),
        'product_type_parent_default': lambda self, cr, uid, ct: eval(
            self.pool['ir.config_parameter'].get_param(cr, uid, 'tianv.product.type.parent', 'False', ct)),
        'order_tax_default': lambda self, cr, uid, ct: eval(
            self.pool['ir.config_parameter'].get_param(cr, uid, 'interface.order.tax.default', 'False', ct)),
        'order_delivery_default': lambda self, cr, uid, ct: eval(
            self.pool['ir.config_parameter'].get_param(cr, uid, 'interface.order.delivery.default', 'False', ct)),
        'order_user_default': lambda self, cr, uid, ct: eval(
            self.pool['ir.config_parameter'].get_param(cr, uid, 'interface.order.user.default', 'False', ct)),
        'delivery_company_code': lambda self, cr, uid, ct: eval(
            self.pool['ir.config_parameter'].get_param(cr, uid, 'interface.delivery.company.code', 'False', ct)),
    }

    @api.multi
    def set_default_info(self):
        self.env['ir.config_parameter'].set_param('tianv.product.type', str(self.product_type_default))
        self.env['ir.config_parameter'].set_param('tianv.product.parent.type', str(self.product_type_parent_default))
        self.env['ir.config_parameter'].set_param('interface.partner.company.default', str(self.partner_company_default.id))
        self.env['ir.config_parameter'].set_param('interface.warehouse.company.default', str(self.partner_warehouse_default.id))
        self.env['ir.config_parameter'].set_param('interface.order.tax.default', str(self.order_tax_default.id))
        self.env['ir.config_parameter'].set_param('interface.order.delivery.default', str(self.order_delivery_default.id))
        self.env['ir.config_parameter'].set_param('interface.order.user.default', str(self.order_user_default.id))
        self.env['ir.config_parameter'].set_param('interface.delivery.company.code', str(self.delivery_company_code))

    @api.multi
    def button_sync_partner(self):
        self.env['res.partner'].sync_tianv_data()

    @api.multi
    def button_sync_order(self):
        self.env['sale.order'].sync_tianv_data()

    @api.multi
    def button_sync_payment(self):
        self.env['xiao.website.pay.log'].sync_tianv_data()

    @api.model
    def cron_sync(self):
        try:
            self.env.cr.execute('SAVEPOINT sync_partners')
            self.env['res.partner'].sync_tianv_data()
            self.env['sale.order'].sync_tianv_data()
        except Exception, e:
            self.env['interface.sync.log'].error('sync.cron', str(e))
            self.env.cr.execute('ROLLBACK TO SAVEPOINT sync_partners')
        self.env.cr.execute('RELEASE SAVEPOINT sync_partners')
