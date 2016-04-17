# author = matt.cai(cysnake4713@gmail.com)
# coding=utf-8
# coding=utf-8
from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _


class Purchase(osv.Model):
    _name = 'purchase.order.line'
    _inherit = 'purchase.order.line'

    _columns = {
        'purchase_show_qty': fields.float(u'对供应商采购数量'),
    }

    def onchange_product_id(self, cr, uid, ids, pricelist_id, product_id, qty, uom_id,
                            partner_id, date_order=False, fiscal_position_id=False, date_planned=False,
                            name=False, price_unit=False, state='draft', context=None):
        res = super(Purchase, self).onchange_product_id(cr, uid, ids, pricelist_id, product_id, qty, uom_id,
                                                        partner_id, date_order, fiscal_position_id, date_planned,
                                                        name, price_unit, state, context)
        res['value'].update({
            'price_unit': self.pool.get('product.product').browse(cr, uid, product_id, context=context).standard_price
        })
        return res
