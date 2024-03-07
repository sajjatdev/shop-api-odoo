import json
from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError
from odoo.addons.website_sale.controllers.main import WebsiteSale
# from addons.website_sale.controllers.main import WebsiteSale


class ProductController(WebsiteSale):
    @http.route('/api/v1/product/list', type='json', auth='public', methods=['GET'], csrf=True)
    def product_list(self, **kwargs):
        products = request.env['product.template'].sudo().search([])  # Fetch all product records
        product_data = []

        # Get all fields of the product template model
        fields = request.env['product.template'].sudo().fields_get()

        for product in products:
            product_dict = {}
            for field_name, field_value in fields.items():
                if field_value['store']:
                    if field_value['type'] == 'many2one':
                        related_record = getattr(product, field_name)
                        if related_record:
                            product_dict[field_name] = {
                                'id': related_record.id,
                               
                            }
                        else:
                            product_dict[field_name] = False
                    elif field_value['type'] == 'one2many':
                        one2many_records = getattr(product, field_name)
                        product_dict[field_name] = [{
                            'id': record.id,
                           
                        } for record in one2many_records]
                    elif field_value['type'] == 'many2many':
                        many2many_records = getattr(product, field_name)
                        product_dict[field_name] = [{
                            'id': record.id,
                            
                        } for record in many2many_records]
                    else:
                        product_dict[field_name] = getattr(product, field_name)
            product_data.append(product_dict)

        return product_data
    

    @http.route('/api/v1/add_to_cart', type='json', auth='public', methods=['POST'], csrf=True)
    def cart_add_item(self, **kwargs):
        try:
            request_json = json.loads(request.httprequest.data)
        except ValueError:
            return request.make_response("Invalid JSON body", headers=[('Content-Type', 'application/json')], status=400)
        
    
        product_id=request_json.get("product_id")
        partner_id=request_json.get("partner_id")
        quantity=request_json.get("quantity")
        
        order = request.env['sale.order'].sudo().search([("access_token","=",request.session.sid)], limit=1)
    

        if not order or order.state != 'draft':
             order= request.env['sale.order'].sudo().create({"access_token":request.session.sid,"website_id":1,"partner_id":partner_id})
        
        order_line=None

        if order:
          order_line= order._cart_update(product_id=product_id, add_qty=1, set_qty=quantity,)
           
        return order_line
    
    @http.route('/api/v1/cart_get', type='json', auth='public', methods=['POST'], csrf=True)
    def cart_get_item(self, **kwargs):
       
        order = request.env['sale.order'].sudo().search([("access_token","=",request.session.sid)], limit=1)
        cart_dict={}
        fields = request.env['sale.order'].sudo().fields_get()
        for field_name, field_value in fields.items():
                if field_value['store']:
                    if field_value['type'] == 'many2one':
                        related_record = getattr(order, field_name)
                        if related_record:
                            cart_dict[field_name] = {
                                'id': related_record.id,
                               
                            }
                        else:
                            cart_dict[field_name] = False
                    elif field_value['type'] == 'one2many':
                        one2many_records = getattr(order, field_name)
                        cart_dict[field_name] = [{
                            'id': record.id,
                           
                        } for record in one2many_records]
                    elif field_value['type'] == 'many2many':
                        many2many_records = getattr(order, field_name)
                        cart_dict[field_name] = [{
                            'id': record.id,
                            
                        } for record in many2many_records]
                    else:
                        cart_dict[field_name] = getattr(order, field_name)

        ## cart iltem list get
        cart_item_list=request.env['sale.order.line'].sudo().search([("order_id","=",order.id)])
        fields_line = request.env['sale.order.line'].sudo().fields_get()

        cart_items=[]
        for cart_item in cart_item_list:
             cart_item_dict={}
             for field_name, field_value in fields_line.items():
                if field_value['store']:
                    if field_value['type'] == 'many2one':
                        related_record = getattr(cart_item, field_name)
                        if related_record:
                            cart_item_dict[field_name] = {
                                'id': related_record.id,
                            }
                        else:
                            cart_item_dict[field_name] = False
                    elif field_value['type'] == 'one2many':
                        one2many_records = getattr(cart_item, field_name)
                        cart_item_dict[field_name] = [{
                            'id': record.id, 
                        } for record in one2many_records]
                    elif field_value['type'] == 'many2many':
                        many2many_records = getattr(cart_item, field_name)
                        cart_item_dict[field_name] = [{
                            'id': record.id,
                            
                        } for record in many2many_records]
                    else:
                        cart_item_dict[field_name] = getattr(cart_item, field_name)

             cart_items.append(cart_item_dict)  

        cart_dict['cart_items']=cart_items
        return cart_dict
    
    @http.route('/api/v1/cart_clear', type='json', auth='public', methods=['POST'], csrf=True)
    def cart_clear(self, **kwargs):
        order = request.env['sale.order'].sudo().search([("access_token","=",request.session.sid)], limit=1)
        for line in order.order_line:
            line.unlink()
        return{"status_code":200,"message":"successfully clear cart"}





