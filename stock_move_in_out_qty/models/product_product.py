# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def button_move_with_in_out_qty(self):
        self.ensure_one()
        action = self.env.ref(
            'stock_move_in_out_qty.action_stock_move_in_out_qty').read()[0]
        action['domain'] = [('product_id', '=', self.id)]
        return action
