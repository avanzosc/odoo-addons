# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    created_repair_id = fields.Many2one(
        string="Created repair", comodel_name="repair.order", copy=False)

    def catch_values_from_create_repair_from_picking(self):
        vals = {'partner_id': self.picking_id.partner_id.id,
                'product_id': self.product_id.id,
                'product_qty': self.qty_done,
                'product_uom': self.product_uom_id.id,
                'location_id': self.location_dest_id.id,
                'created_from_move_line_id': self.id}
        if self.lot_id:
            vals['lot_id'] = self.lot_id.id
        if self.picking_id.sale_order_id:
            vals['sale_order_id'] = self.picking_id.sale_order_id.id
        if self.picking_id.origin:
            cond = [('name', '=', self.picking_id.origin)]
            purchase = self.env['purchase.order'].search(cond, limit=1)
            if purchase:
                vals['purchase_order_id'] = purchase.id
        return vals
