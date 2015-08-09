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
