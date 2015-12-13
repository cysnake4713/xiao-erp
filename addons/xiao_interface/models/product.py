# -*- coding: utf-8 -*-
# author: cysnake4713
#

from openerp import tools
from openerp import models, fields, api
from openerp.tools.translate import _
from ..tianvlib import product_client as client
import json


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    tianv_id = fields.Integer('Tianv ID')

    @api.multi
    def create_and_update_template(self):
        tianv_value_obj = self.env['product.template.tianv.value']
        for template in self:
            # sync product info
            # update
            if template.tianv_id:
                product_value = client.GetProduct(id=template.tianv_id)
                product_value.update({
                    "Title": template.name,
                    'Attribute_infos': [],
                    'Product_Number_Infos': [],
                })
                client.EditProduct(product=json.dumps(product_value))
            # create
            else:
                product_value = {
                    "id": 0,
                    "Title": template.name,
                    "Price": 0,
                    "TypeId": int(self.env['ir.config_parameter'].get_param('tianv.product.type')),
                    'Attribute_infos': [],
                    'Product_Number_Infos': [],
                    "ProductType": u"实物产品",
                }
                result = client.AddProduct(product=json.dumps(product_value))
                template.tianv_id = int(result['Msg'])
            # sync attr & param info
            param_value = [{'id': l.tianv_id,
                            'odooId': l.id,
                            'Min': 0,
                            'Max': 0,
                            'Product_Info_id': template.tianv_id,
                            'AttributeName': l.attribute_id.name,
                            'IsNum': u'型号',
                            'rule': u'单选',
                            'Type': u'默认类型',
                            'Parameter_Infos': [{"id": tianv_value_obj.get_tianv_id(template.id, v.id),
                                                 "odooId": v.id,
                                                 "Att_Info_id": l.tianv_id,
                                                 "ParameterName": v.name,
                                                 "ImageFile": None,
                                                 "colorValue": None,
                                                 "TextValue": v.name,
                                                 "Coefficient": 0,
                                                 "proId": template.tianv_id,
                                                 "Remark": "",
                                                 "Number": -1,
                                                 "def": u"不选",
                                                 } for v in l.value_ids],
                            } for l in template.attribute_line_ids]
            client.sync_product_param(product_id=template.tianv_id, json=json.dumps(param_value))
            result = client.GetProduct(id=template.tianv_id)['Attribute_infos']
            # clear all value map
            tianv_value_obj.search([('template_id', '=', template.id)]).unlink()
            for attr in result:
                template.attribute_line_ids.filtered(lambda tl: tl.id == attr['odooId']).tianv_id = attr['id']
                # generate new value map
                for param in attr['Parameter_Infos']:
                    tianv_value_obj.set_tianv_id(template.id, param['odooId'], param['id'])
            # sync stock & price
            # delete old stock info
            client.DelProduct_Number(id=template.tianv_id)
            # add new info
            for p in self.env['product.product'].search([('product_tmpl_id', '=', template.id)]):
                number_info_value = {"id": 0,
                                     "Product_Info_id": template.tianv_id,
                                     "parIds": ','.join([str(tianv_value_obj.get_tianv_id(template.id, v.id)) for v in p.attribute_value_ids]),
                                     "parNames": ','.join([v.name for v in p.attribute_value_ids]),
                                     "Number": int(p.qty_available),
                                     "Price": p.lst_price,
                                     "odoocode": p.default_code,
                                     }
                client.AddOrEditProduct_Number_Info(proid=template.tianv_id, Product_Number_InfoJson=json.dumps(number_info_value))


class ProductAttrLine(models.Model):
    _inherit = 'product.attribute.line'

    tianv_id = fields.Integer('Tianv ID')


class ProductAttrLineValue(models.Model):
    _name = 'product.template.tianv.value'

    template_id = fields.Many2one('product.template', 'Template', required=True)
    val_id = fields.Many2one('product.attribute.value', 'Value', required=True)
    tianv_id = fields.Integer('Tianv ID')

    @api.model
    def get_tianv_id(self, template_id, val_id):
        result = self.env['product.template.tianv.value'].search([('template_id', '=', template_id), ('val_id', '=', val_id)])
        if result:
            return result.tianv_id
        else:
            return 0

    @api.model
    def set_tianv_id(self, template_id, val_id, tianv_id):
        self.create({
            'template_id': template_id,
            'val_id': val_id,
            'tianv_id': tianv_id,
        })
