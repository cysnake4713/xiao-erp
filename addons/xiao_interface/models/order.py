# -*- coding: utf-8 -*-
# author: cysnake4713
#

from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _
from ..tianvlib import product_client as client
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    tianv_id = fields.Integer('Tianv ID')
    delivery_address = fields.Char('Delivery Address')
    delivery_name = fields.Char('Delivery Name')
    delivery_phone = fields.Char('Delivery Phone')
    pay_method = fields.Char('Pay Method')
    tianv_order_date = fields.Char('Tianv Order Date')
    deliveryPrice = fields.Float('Delivery Price')
    invoice_type = fields.Char('Invoice Type')
    tianv_state = fields.Char('Tianv State')

    @api.model
    def sync_tianv_data(self):
        last_update = self.env['ir.config_parameter'].get_param('interface.order.last.update', 'False')
        if last_update == 'False':
            order_ids = client.GetOrderIds()['ids']
        else:
            order_ids = client.GetOrderIds(updateTime=last_update)['ids']
        for tianv_id in order_ids:
            tianv_values = client.GetOrderById(id=tianv_id)
            order_id = self.search([('tianv_id', '=', tianv_id)])
            partner_id = self.env['res.partner'].search([('is_company', '=', False), ('tianv_id', '=', tianv_values['userId'])])
            if not (partner_id and len(partner_id) == 1):
                _logger.error('miss match partner tianv id:%s' % tianv_values['userId'])
                partner_id = eval(self.env['ir.config_parameter'].get_param('interface.partner.company.default', 'False'))
            else:
                partner_id = partner_id.id
            if order_id:
                order_id.update({
                    'tianv_id': tianv_id,
                    'partner_id': partner_id,
                    'delivery_address': tianv_values['address'],
                    'delivery_name': tianv_values['name'],
                    'delivery_phone': tianv_values['phone'],
                    'pay_method': tianv_values['payMethod'],
                    'tianv_order_date': tianv_values['date'],
                    'deliveryPrice': tianv_values['deliveryPrice'],
                    'invoice_type': tianv_values['invoiceType'],
                    'tianv_state': tianv_values['state'],
                })
                # TODO: what to do with product and transfer price?
            else:
                order_id = self.create({
                    'tianv_id': tianv_id,
                    'partner_id': partner_id,
                    'delivery_address': tianv_values['address'],
                    'delivery_name': tianv_values['name'],
                    'delivery_phone': tianv_values['phone'],
                    'pay_method': tianv_values['payMethod'],
                    'tianv_order_date': tianv_values['date'],
                    'deliveryPrice': tianv_values['deliveryPrice'],
                    'invoice_type': tianv_values['invoiceType'],
                    'tianv_state': tianv_values['state'],
                    'company_id': eval(self.env['ir.config_parameter'].get_param('interface.partner.company.default', 'False')),
                    'warehouse_id': eval(self.env['ir.config_parameter'].get_param('interface.warehouse.company.default', 'False')),
                    # 'state': tianv_values['state'],

                })
                for line in tianv_values['orderLines']:
                    product_id = self.env['product.product'].search([('tianv_id', '=', line['productId'])])
                    if not (product_id and len(product_id) == 1):
                        _logger.error('miss match product tianv id:%s' % line['productId'])
                        product_name = line['productName']
                        product_id = False
                        product_uom = 1
                    else:
                        product_name = product_id.name
                        product_id = product_id.id
                        product_uom = product_id.uom_id.id
                    self.env['sale.order.line'].create({
                        'order_id': order_id.id,
                        'product_id': product_id,
                        'name': product_name,
                        'product_uom_qty': line['qty'],
                        'price_unit': line['price'],
                        'product_uom': product_uom,
                    })
                    # TODO: transfer price
        self.env['ir.config_parameter'].set_param('interface.order.last.update', fields.Datetime.now())
