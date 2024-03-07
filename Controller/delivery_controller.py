import json
from odoo import api,http
from odoo.http import request
from odoo.addons.website_sale.controllers.delivery import WebsiteSaleDelivery

class DeliveryController(WebsiteSaleDelivery):

    @http.route(['/api/v1/update_carrier'], type='json', auth='public', methods=['POST'], csrf=True)
    def update_eshop_carrier(self, **post):
        try:
            request_json = json.loads(request.httprequest.data)
        except ValueError:
            return request.make_response("Invalid JSON body", headers=[('Content-Type', 'application/json')], status=400)
        

        carrier_id = int(request_json.get("carrier_id"))

        order = request.env['sale.order'].sudo().search([("access_token","=",request.session.sid)], limit=1)
    
        order.write({'carrier_id':carrier_id})

        carrier = request.env['delivery.carrier'].sudo().browse(int(carrier_id))
        shipping_list=request.env['sale.order.line'].sudo().search([('order_id','=',order.id),('is_delivery','=',True)])
        
  
        if len(shipping_list)!=0:
            for shipping in shipping_list:
                for product in carrier.product_id:
                    shipping.write({'product_id':product.id})
                 
        else:
            for product in carrier.product_id:
                 request.env['sale.order.line'].sudo().create({'order_id':order.id,"is_delivery":True,'product_id':product.id})

        if order:
            return carrier.product_id.id
        else:
            return {}


