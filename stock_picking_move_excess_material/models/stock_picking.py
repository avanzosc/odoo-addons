# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def action_move_excess_material(self):
        cond = [('location_id', '=', self.location_id.id),
                ('quantity', '>', 0)]
        quants = self.env['stock.quant'].search(cond)
        products = quants.mapped('product_id')
        for product in products:
            product_quants = quants.filtered(
                lambda x: x.product_id.id == product.id)
            quantity = sum(product_quants.mapped('quantity'))
            reserved_quantity = sum(product_quants.mapped('reserved_quantity'))
            if quantity - reserved_quantity > 0:
                vals = self._catch_values_for_excess_material(
                    product, quantity, reserved_quantity)
                self.env['stock.move'].create(vals)

    def _catch_values_for_excess_material(self, product, quantity,
                                          reserved_quantity):
        vals = {
            'picking_id': self.id,
            'product_id': product.id,
            'name': product.name,
            'product_uom': product.uom_id.id,
            'location_id': self.location_id.id,
            'location_dest_id': self.location_dest_id.id,
            'product_uom_qty': quantity - reserved_quantity}
        return vals
