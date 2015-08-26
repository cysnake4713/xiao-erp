# -*- coding: utf-8 -*-
# author: cysnake4713
#
from openerp import http
from openerp.http import request
import werkzeug.utils
import logging
from datetime import datetime
import time
from werkzeug.exceptions import HTTPException, NotFound

_logger = logging.getLogger(__name__)


class StockWebsite(http.Controller):
    @http.route('/mobile/stock/scan/list/<code>', type='http', auth='user_wechat')
    def stock_list(self, code, **kw):
        client = request.registry['odoosoft.wechat.enterprise.account'].get_client(request.cr, request.uid, code, context=request.context)
        if client:
            noncestr = 'Wm3WZYTPz0wzccnW'
            ticket = client.jsapi.get_jsapi_ticket()
            timestamp = client.jsapi.session.get('jsapi_ticket_expires_at', 0)
            url = request.httprequest.base_url
            config = {
                'corp_id': client.corp_id,
                'noncestr': noncestr,
                'timestamp': timestamp,
                'signature': client.jsapi.get_jsapi_signature(noncestr, ticket, timestamp, url),
                'debug': 'true' if 'debug' in kw else 'false',

            }
            # process list
            picking_ids = request.registry['stock.picking'].search(request.cr, request.uid,
                                                                   [('state', 'in', ['confirmed', 'partially_available', 'assigned'])],
                                                                   order='id desc',
                                                                   context=request.context)
            result = request.registry['stock.picking'].browse(request.cr, request.uid, picking_ids, context=request.context)

            return request.render('xiao_wechat_stock.stock_list', qcontext={'config': config, 'result': result, 'code': code})
        else:
            return NotFound()

    @http.route('/mobile/stock/scan/detail/<code>/<id>', type='http', auth='user_wechat')
    def stock_form(self, code, id, **kw):
        client = request.registry['odoosoft.wechat.enterprise.account'].get_client(request.cr, request.uid, code, context=request.context)
        if client:
            noncestr = 'Wm3WZYTPz0wzccnW'
            ticket = client.jsapi.get_jsapi_ticket()
            timestamp = client.jsapi.session.get('jsapi_ticket_expires_at', 0)
            url = request.httprequest.base_url
            config = {
                'corp_id': client.corp_id,
                'noncestr': noncestr,
                'timestamp': timestamp,
                'signature': client.jsapi.get_jsapi_signature(noncestr, ticket, timestamp, url),
                'debug': 'true' if 'debug' in kw else 'false',

            }
            picking_obj = request.registry['stock.picking']

            result = picking_obj.browse(request.cr, request.uid, int(id), context=request.context)
            return request.render('xiao_wechat_stock.stock_form', qcontext={'config': config, 'result': result, 'code': code})
        return NotFound()

    @http.route('/mobile/stock/scan/update', type='http', auth='user_wechat')
    def update_data(self, **kw):
        picking_obj = request.registry['stock.picking']
        message = ''
        oid = kw['id']
        if 'update_state' in kw:
            try:
                picking_obj.action_assign(request.cr, request.uid, [int(oid)], context=request.context)
            except Exception, e:
                message += e.message
                _logger.error('Wechat Stock State Check Error: %s', e)

        if 'update_carrier_ref' in kw:
            try:
                picking_obj.write(request.cr, request.uid, [int(oid)], {'carrier_tracking_ref': kw['update_carrier_ref']}, context=request.context)
            except Exception, e:
                message += e.message
                _logger.error('Wechat Stock State Check Error: %s', e)

        if 'transfer_all' in kw:
            wizard_view = picking_obj.do_enter_transfer_details(request.cr, request.uid, [int(oid)], context=request.context)
            wizard = request.registry['stock.transfer_details'].browse(request.cr, request.uid, wizard_view['res_id'], context=request.context)
            wizard.do_detailed_transfer()
        return message
