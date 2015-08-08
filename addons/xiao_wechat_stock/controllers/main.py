# -*- coding: utf-8 -*-
# author: cysnake4713
#
from openerp import http
from openerp.http import request
import werkzeug.utils
import logging
from datetime import datetime
import time

_logger = logging.getLogger(__name__)


class StockWebsite(http.Controller):
    @http.route('/mobile/stock/scan/<code>', type='http', auth='user_wechat')
    def stock_scan(self, code):
        client = request.registry['odoosoft.wechat.enterprise.account'].get_client(request.cr, request.uid, code, context=request.context)
        if client:
            noncestr = 'Wm3WZYTPz0wzccnW'
            timestamp = int(time.mktime(datetime.now().timetuple()))
            url = '/mobile/stock/scan/%s' % code
            config = {
                'corp_id': client.corp_id,
                'noncestr': noncestr,
                'timestamp': timestamp,
                'signature': client.jsapi.get_jsapi_signature(noncestr, client.jsapi.get_jsapi_ticket(), timestamp, url)

            }
            return request.render('xiao_wechat_stock.scan', qcontext={'config': config})
