from odoo import fields,api,models
from odoo.addons.sale.models.sale_order import SALE_ORDER_STATE

class SaleOrderModel(models.Model):
      
    _inherit = 'sale.order'

    state = fields.Selection(
        selection=SALE_ORDER_STATE,
        string="Status",
        index=True,
        default='draft'
    )

    def action_send(self):
        self.write({'state':'sent'})

    def action_confirm(self):
        self.write({'state':"sale"})

    def action_cancel(self):
        self.write({'state':"cancel"})

    
        
       
        