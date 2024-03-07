import json
from odoo import api,http
from odoo.http import request,Response

class OrderStatusController(http.Controller):

    @http.route('/api/v1/order_sent', type='json', auth='user', methods=['POST'], csrf=True)
    def order_sent(self, **kwargs):
        try:
          order = request.env['sale.order'].sudo().search([("access_token","=",request.session.sid)], limit=1)
          order.ensure_one()
          
          if order.state in ('draft'):
               order.action_send()
               return{"status_code":200,"message":"order sent succesfully"}
          else:
               return {"status_code":409,"message":f"{order.state} is the order state."}
        except:
             return {"status_code":401,"message":"Unauthorized"}
    
    @http.route('/api/v1/order_confirm', type='json', auth='user', methods=['POST'], csrf=True)
    def order_confirm(self, **kwargs):
        try:
          order = request.env['sale.order'].sudo().search([("access_token","=",request.session.sid)], limit=1)
          order.ensure_one()
          if order.state is ('draft','sent'):
               order.action_confirm()
               return{"status_code":200,"message":"successfully confirmed the order"}
          else:
               return {"status_code":409,"message":f"{order.state} is the order state."}
        except:
             return {"status_code":401,"message":"Unauthorized"}
        
    
    @http.route('/api/v1/order_cancel', type='json', auth='user', methods=['POST'], csrf=True)
    def order_cancel(self, **kwargs):
        try:
          order = request.env['sale.order'].sudo().search([("access_token","=",request.session.sid)], limit=1)
          order.ensure_one()

          if order.state not in ('sale'):
                    if order.state != 'cancel':
                              order.action_cancel()
                    return{"status_code":200,"message":"Order cancellation completed"}
          else:
               return {"status_code":409,"message":f"{order.state} is the order state."}
        except:
             return {"status_code":401,"message":"Unauthorized"}
     
