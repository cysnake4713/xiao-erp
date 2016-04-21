# coding=utf-8
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _
from ..tianvlib import product_client as client


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    delivery_address = fields.Char('Delivery Address')
    delivery_name = fields.Char('Delivery Name')
    delivery_phone = fields.Char('Delivery Phone')
    deliveryPrice = fields.Float('Delivery Price')
    carrier_tracking_ref = fields.Char('Carrier Tracking Ref')

    @api.multi
    def button_update_delivery(self):
        if self.origin:
            origin_sale_order = self.env['sale.order'].search([('name', '=', self.origin)])
            if origin_sale_order.tianv_id and self.carrier_tracking_ref:
                logistics_id = self.env.ref('xiao_interface.param_tianv_delivery_company_code').value
                client.UpdateOrderLogistics(orderid=origin_sale_order.tianv_id, LogisticsId=logistics_id, LogisticsTicketNo=self.carrier_tracking_ref,
                                            Time=fields.Datetime.now())
        return True
