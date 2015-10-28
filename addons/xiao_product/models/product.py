# -*- coding: utf-8 -*-
# author: cysnake4713
#
from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp


class Product(models.Model):
    _inherit = 'product.product'

    retail_price = fields.Float('Retail Price', digits=dp.get_precision('Product Price'))
    store_lst_price = fields.Float('Stored Lst Price', digits=dp.get_precision('Product Price'), )
    lst_price = fields.Float('Lst Price', digits=dp.get_precision('Product Price'), compute='_get_lst_price', inverse='_set_lst_price')

    # weight
    volume = fields.Float('Volume', help="The volume in m3.")
    weight = fields.Float('Gross Weight', digits=dp.get_precision('Stock Weight'), help="The gross weight in Kg.")
    weight_net = fields.Float('Net Weight', digits=dp.get_precision('Stock Weight'), help="The net weight in Kg.")

    # stock location
    loc_rack = fields.Char('Rack', size=16)
    loc_row = fields.Char('Row', size=16)
    loc_case = fields.Char('Case', size=16)
    description = fields.Text('Description')

    @api.one
    @api.depends('store_lst_price')
    def _get_lst_price(self):
        self.lst_price = self.store_lst_price

    @api.one
    def _set_lst_price(self):
        self.store_lst_price = self.lst_price


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.v7
    def _price_get(self, cr, uid, products, ptype='list_price', context=None):
        res = super(ProductTemplate, self)._price_get(cr, uid, products, ptype, context)
        for product in products:
            res[product.id] = product.sudo()['lst_price']
        return res

    _defaults = {
        'type': 'product',
        'cost_method': 'real',
        'valuation': 'real_time',
    }
