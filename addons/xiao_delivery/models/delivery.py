# -*- coding: utf-8 -*-
# author: cysnake4713
#

from openerp import tools, exceptions
from openerp import models, fields, api
from openerp.tools.translate import _


class DeliveryGridLine(models.Model):
    _inherit = 'delivery.grid.line'

    first_price = fields.Float('First Price')
    first_value = fields.Float('First Value')


class DeliveryGrid(models.Model):
    _inherit = 'delivery.grid'

    @api.v7
    def get_price_from_picking(self, cr, uid, id, total, weight, volume, quantity, context=None):
        grid = self.browse(cr, uid, id, context=context)
        price = 0.0
        ok = False
        price_dict = {'price': total, 'volume': volume, 'weight': weight, 'wv': volume * weight, 'quantity': quantity}
        for line in grid.line_ids:
            test = eval(line.type + line.operator + str(line.max_value), price_dict)
            if test:
                if line.price_type == 'variable':
                    if line.first_value:
                        if price_dict[line.variable_factor] > line.first_value:
                            price = line.first_price * line.first_value + line.list_price * (price_dict[line.variable_factor] - line.first_value)
                        else:
                            price = line.first_price * line.first_value
                    else:
                        price = line.list_price * price_dict[line.variable_factor]
                else:
                    price = line.list_price
                ok = True
                break
        if not ok:
            raise exceptions.Warning(_("Unable to fetch delivery method!"),
                                     _("Selected product in the delivery method doesn't fulfill any of the delivery grid(s) criteria."))

        return price
