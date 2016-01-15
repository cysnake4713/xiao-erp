# author = matt.cai(cysnake4713@gmail.com)
# coding=utf-8
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _
from ..tianvlib import product_client as client
import logging

_logger = logging.getLogger(__name__)


class WebsitePayLog(models.Model):
    _inherit = 'xiao.website.pay.log'

    @api.model
    def sync_tianv_data(self):

        last_update = self.env['ir.config_parameter'].get_param('interface.payment.last.update', 'False')
        if last_update == 'False':
            tianv_records = client.GetUserGoldIds()['ids']
        else:
            tianv_records = client.GetUserGoldIds(UpdateTime=last_update)['ids']

        for tianv_id in tianv_records:
            tianv_values = client.GetUserGoldById(id=tianv_id)
            log_id = self.search([('tianv_id', '=', tianv_id)])
            # if exist
            if log_id:
                log_id.update({
                    'tianv_id': tianv_id,
                    'related_order_ids': [(6, 0,
                                           [o.id for o in self.env['sale.order'].search([('tianv_id', 'in', tianv_values['orderIds'])])]
                                           )],
                    'closed_order_ids': [(6, 0,
                                          [o.id for o in self.env['sale.order'].search([('tianv_id', 'in', tianv_values['closedOrderIds'])])]
                                          )],
                    'price': tianv_values['amount'],
                    'pay_datetime': tianv_values['date'],
                })
            else:
                self.create({
                    'tianv_id': tianv_id,
                    'related_order_ids': [(6, 0,
                                           [o.id for o in self.env['sale.order'].search([('tianv_id', 'in', tianv_values['orderIds'])])]
                                           )],
                    'closed_order_ids': [(6, 0,
                                          [o.id for o in self.env['sale.order'].search([('tianv_id', 'in', tianv_values['closedOrderIds'])])]
                                          )],
                    'price': tianv_values['amount'],
                    'pay_datetime': tianv_values['date'],
                })
        self.env['ir.config_parameter'].set_param('interface.order.last.update', fields.Datetime.now())
