import json
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
# from addons.website_sale.controllers.main import WebsiteSale
class ProductController(WebsiteSale):
    @http.route('/api/v1/product/list', type='json', auth='none', methods=['GET'], csrf=True)
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
    

    @http.route('/api/v1/cart/add', type='json', auth='none', methods=['POST'], csrf=True)
    def cart_add_item(self, **kwargs):
        try:
            request_json = json.loads(request.httprequest.data)
        except ValueError:
            return request.make_response("Invalid JSON body", headers=[('Content-Type', 'application/json')], status=400)
        
        customer_id=request_json.get("customer_id")
        product_id=request_json.get("product_id")
        quantity=request_json.get("quantity")

        cart = request.env['sale.order'].sudo().create({'partner_id': customer_id,})

        cart = request.env['sale.order'].sudo().browse(cart.id)

        if not cart:
            return request.make_response("Cart not found", headers=[('Content-Type', 'application/json')], status=404)


        cart_line = cart.order_line.create({
            'product_id': product_id,
            'product_uom_qty': quantity,
        })

        response_data = {
            'message': 'Item added to cart successfully',
            'cart_id': cart.id,
            'cart_line_id': cart_line.id,
        }
        
        return response_data



