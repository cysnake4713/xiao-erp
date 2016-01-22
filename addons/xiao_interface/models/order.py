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
        is_miss_info = False
        param_obj = self.env['ir.config_parameter']
        last_update = param_obj.get_param('interface.order.last.update', 'False')
        if last_update == 'False':
            order_ids = client.GetOrderIds()['ids']
        else:
            order_ids = client.GetOrderIds(updateTime=last_update)['ids']
        for tianv_id in order_ids:
            tianv_values = client.GetOrderById(id=tianv_id)
            order_id = self.search([('tianv_id', '=', tianv_id)])
            if not order_id:
                partner_id = self.env['res.partner'].search([('is_company', '=', False), ('tianv_id', '=', tianv_values['userId'])])
                if not (partner_id and len(partner_id) == 1):
                    log_partner_info = 'miss match partner tianv id:%s' % tianv_values['userId']
                    _logger.error(log_partner_info)
                    order_id.message_post(body=log_partner_info)
                    partner_id = eval(param_obj.get_param('interface.partner.company.default', 'False'))
                    is_miss_info = True
                else:
                    partner_id = partner_id.id
                order_id = self.create({
                    'tianv_id': tianv_id,
                    'partner_id': partner_id,
                    'delivery_address': tianv_values['address'],
                    'delivery_name': tianv_values['name'],
                    'delivery_phone': tianv_values['phone'],
                    'pay_method': tianv_values['payMethod'],
                    'tianv_order_date': fields.Datetime.to_string(fields.Datetime.from_string(tianv_values['date'])),
                    'deliveryPrice': tianv_values['deliveryPrice'],
                    'invoice_type': tianv_values['invoiceType'],
                    'tianv_state': tianv_values['state'],
                    'company_id': eval(param_obj.get_param('interface.partner.company.default', 'False')),
                    'warehouse_id': eval(param_obj.get_param('interface.warehouse.company.default', 'False')),
                    # 'state': tianv_values['state'],

                })
                order_id.message_post(body=log_partner_info)
                tax_id = eval(param_obj.get_param('interface.order.tax.default', 'False'))
                for line in tianv_values['orderLines']:
                    product_id = self.env['product.product'].search([('tianv_id', '=', line['productId'])])
                    if not (product_id and len(product_id) == 1):
                        log_info = 'miss match product tianv id:%s' % line['productId']
                        _logger.error(log_info)
                        order_id.message_post(body=log_info)
                        is_miss_info = True
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
                        'tax_id': [(6, 0, [tax_id])] if tianv_values['invoiceType'] not in [u'无需发票'] else False,
                    })
                    # add delivery price
                    delivery_id = eval(param_obj.get_param('interface.order.delivery.default', 'False'))
                    self.env['sale.order.line'].create({
                        'order_id': order_id.id,
                        'product_id': delivery_id,
                        'name': u'运费',
                        'product_uom_qty': 1,
                        'price_unit': tianv_values['deliveryPrice'],
                        'product_uom': 1,
                        # 'tax_id': [(6, 0, [tax_id])] if tianv_values['invoiceType'] not in [u'无需发票'] else False,
                    })
                if not is_miss_info:
                    order_id.action_button_confirm()
                    # todo: need add address in picking and update tianv stock number
        param_obj.set_param('interface.order.last.update', fields.Datetime.now())
