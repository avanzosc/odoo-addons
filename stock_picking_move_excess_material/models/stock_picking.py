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
        for quant in quants:
            if quant.quantity - quant.reserved_quantity > 0:
                vals = self._catch_values_for_excess_material(quant)
                self.env['stock.move'].create(vals)

    def _catch_values_for_excess_material(self, quant):
        vals = {
            'picking_id': self.id,
            'product_id': quant.product_id.id,
            'name': quant.product_id.name,
            'product_uom': quant.product_id.uom_id.id,
            'location_id': self.location_id.id,
            'location_dest_id': self.location_dest_id.id,
            'product_uom_qty': quant.quantity - quant.reserved_quantity}
        return vals
